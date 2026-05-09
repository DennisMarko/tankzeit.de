#!/usr/bin/env python3
"""Rank customer-friendly fuel stations from the local tankzeit snapshot.

The score intentionally uses only consumer-facing criteria:

1. price level at the current noon reference
2. price stability from the station's intraday span
3. markdown speed after the 12:00 reset

Outputs:
- output/customer_friendliness/station_customer_friendliness.csv
- output/customer_friendliness/station_fuel_customer_friendliness.csv
- output/customer_friendliness/brand_customer_friendliness.csv
- output/customer_friendliness/customer_friendliness_report.md
- data/customer_friendliness_awards.json
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
FUELS = ("diesel", "e10", "e5")
FUEL_LABELS = {"diesel": "Diesel", "e10": "E10", "e5": "E5"}
DEFAULT_OUTPUT_DIR = ROOT / "output" / "customer_friendliness"
DEFAULT_AWARDS_PATH = ROOT / "data" / "customer_friendliness_awards.json"
MIN_MARKDOWN_EUR = 0.005
NO_MARKDOWN_SENTINEL_HOUR = 25.0
AWARD_TIERS = (
    ("gold", "Gold", 0.02),
    ("silver", "Silber", 0.05),
    ("bronze", "Bronze", 0.10),
)


@dataclass(frozen=True)
class Station:
    uuid: str
    name: str
    brand: str
    city: str
    post_code: str
    street: str
    house_number: str


@dataclass(frozen=True)
class NoonSnapshot:
    prices: dict[str, dict[str, float]]
    latest_update: str


@dataclass(frozen=True)
class Observation:
    station_uuid: str
    fuel: str
    noon_price: float
    span_cents: float
    first_markdown_hour: float | None
    first_markdown_score_value: float
    markdown_by_14_cents: float
    markdown_by_16_cents: float
    markdown_by_18_cents: float
    markdown_by_22_cents: float
    cycle_days: int

    @property
    def key(self) -> tuple[str, str]:
        return self.station_uuid, self.fuel


@dataclass(frozen=True)
class OutputPaths:
    station_csv: Path
    station_fuel_csv: Path
    brand_csv: Path
    report_md: Path
    awards_json: Path


def _positive_float(value: object) -> float | None:
    if value is None:
        return None
    try:
        number = float(str(value).replace(",", "."))
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number) or number <= 0:
        return None
    return number


def _safe_float(value: object, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(number):
        return default
    return number


def _mean(values: Iterable[float]) -> float:
    cleaned = [float(value) for value in values if math.isfinite(float(value))]
    if not cleaned:
        return 0.0
    return statistics.fmean(cleaned)


def _fmt(value: float | int | None, digits: int = 1) -> str:
    if value is None:
        return "keine"
    if isinstance(value, int):
        return str(value)
    return f"{float(value):.{digits}f}"


def _display_brand(raw: object) -> str:
    brand = (str(raw or "").strip() or "Unbekannt")
    return brand


def _station_uuid_from_data2_path(path: Path, data2_dir: Path) -> str:
    relative = path.relative_to(data2_dir)
    if len(relative.parts) < 6:
        raise ValueError(f"Unexpected data2 path layout: {path}")
    return "-".join(relative.parts[:5])


def _data2_station_dir(data2_dir: Path, station_uuid: str) -> Path | None:
    parts = station_uuid.split("-")
    if len(parts) != 5:
        return None
    return data2_dir.joinpath(*parts)


def load_stations(path: Path) -> dict[str, Station]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    stations: dict[str, Station] = {}
    for item in payload:
        uuid = str(item.get("uuid") or "").strip()
        if not uuid:
            continue
        stations[uuid] = Station(
            uuid=uuid,
            name=str(item.get("name") or "").strip(),
            brand=_display_brand(item.get("brand")),
            city=str(item.get("city") or "").strip(),
            post_code=str(item.get("post_code") or "").strip(),
            street=str(item.get("street") or "").strip(),
            house_number=str(item.get("house_number") or "").strip(),
        )
    return stations


def load_noon_snapshot(path: Path, fuels: Sequence[str] = FUELS) -> NoonSnapshot:
    prices: dict[str, dict[str, float]] = defaultdict(dict)
    latest_update = ""
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            station_uuid = str(row.get("station_uuid") or "").strip()
            if not station_uuid:
                continue
            row_update = str(row.get("last_update") or "").strip()
            if row_update > latest_update:
                latest_update = row_update
            for fuel in fuels:
                price = _positive_float(row.get(fuel))
                if price is not None and 0.5 <= price <= 3.5:
                    prices[station_uuid][fuel] = price
    return NoonSnapshot(prices=dict(prices), latest_update=latest_update)


def _payload_span_cents(payload: dict[str, object]) -> float | None:
    span = _positive_float(payload.get("span"))
    if span is not None:
        return span * 100.0

    hourly = payload.get("hourly") or []
    prices = [_safe_float(row.get("price")) for row in hourly if isinstance(row, dict)]
    if len(prices) >= 2:
        return (max(prices) - min(prices)) * 100.0
    return None


def _markdown_value(row: dict[str, object]) -> float:
    markdown = _safe_float(row.get("markdown_median"), default=math.nan)
    if math.isfinite(markdown):
        return max(0.0, markdown)
    delta = _safe_float(row.get("delta_median"), default=0.0)
    return max(0.0, -delta)


def _cycle_rows_by_hour(payload: dict[str, object]) -> dict[int, dict[str, object]]:
    rows: dict[int, dict[str, object]] = {}
    for row in payload.get("cycle_hourly") or []:
        if not isinstance(row, dict):
            continue
        try:
            hour = int(row.get("cycle_hour"))
        except (TypeError, ValueError):
            continue
        rows[hour] = row
    return rows


def _markdown_at(rows_by_hour: dict[int, dict[str, object]], cycle_hour: int) -> float:
    row = rows_by_hour.get(cycle_hour)
    if not row:
        return 0.0
    return _markdown_value(row)


def _first_markdown_hour(rows_by_hour: dict[int, dict[str, object]]) -> float | None:
    for cycle_hour in sorted(hour for hour in rows_by_hour if hour > 0):
        if _markdown_value(rows_by_hour[cycle_hour]) >= MIN_MARKDOWN_EUR:
            return float(cycle_hour)
    return None


def _cycle_days(payload: dict[str, object]) -> int:
    cycle_summary = payload.get("cycle_summary")
    if isinstance(cycle_summary, dict):
        days = _positive_float(cycle_summary.get("days"))
        if days is not None:
            return int(days)
    summary = payload.get("summary")
    if isinstance(summary, dict):
        days = _positive_float(summary.get("days"))
        if days is not None:
            return int(days)
    return 0


def load_observations(
    data2_dir: Path,
    noon_snapshot: NoonSnapshot,
    stations: dict[str, Station],
    fuels: Sequence[str] = FUELS,
) -> list[Observation]:
    observations: list[Observation] = []
    for station_uuid, fuel_prices in noon_snapshot.prices.items():
        if station_uuid not in stations:
            continue
        station_dir = _data2_station_dir(data2_dir, station_uuid)
        if station_dir is None:
            continue
        for fuel in fuels:
            noon_price = fuel_prices.get(fuel)
            if noon_price is None:
                continue
            path = station_dir / f"{fuel}.json"
            if not path.exists():
                continue
            if station_uuid not in stations:
                continue
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue

            span_cents = _payload_span_cents(payload)
            if span_cents is None or span_cents < 0 or span_cents > 150:
                continue

            rows_by_hour = _cycle_rows_by_hour(payload)
            if not rows_by_hour:
                continue

            first_hour = _first_markdown_hour(rows_by_hour)
            observations.append(
                Observation(
                    station_uuid=station_uuid,
                    fuel=fuel,
                    noon_price=noon_price,
                    span_cents=span_cents,
                    first_markdown_hour=first_hour,
                    first_markdown_score_value=(
                        first_hour
                        if first_hour is not None
                        else NO_MARKDOWN_SENTINEL_HOUR
                    ),
                    markdown_by_14_cents=_markdown_at(rows_by_hour, 2) * 100.0,
                    markdown_by_16_cents=_markdown_at(rows_by_hour, 4) * 100.0,
                    markdown_by_18_cents=_markdown_at(rows_by_hour, 6) * 100.0,
                    markdown_by_22_cents=_markdown_at(rows_by_hour, 10) * 100.0,
                    cycle_days=_cycle_days(payload),
                )
            )
    return observations


def _percentile_scores(
    rows: Sequence[Observation],
    value_fn: Callable[[Observation], float],
    *,
    higher_is_better: bool,
) -> dict[tuple[str, str], float]:
    if not rows:
        return {}
    if len(rows) == 1:
        return {rows[0].key: 50.0}

    ordered = sorted((value_fn(row), index, row.key) for index, row in enumerate(rows))
    scores: dict[tuple[str, str], float] = {}
    index = 0
    denominator = len(ordered) - 1
    while index < len(ordered):
        value = ordered[index][0]
        end = index
        while end + 1 < len(ordered) and ordered[end + 1][0] == value:
            end += 1
        average_rank = (index + end) / 2.0
        percentile = average_rank / denominator
        score = percentile if higher_is_better else 1.0 - percentile
        for _, _, key in ordered[index : end + 1]:
            scores[key] = round(score * 100.0, 3)
        index = end + 1
    return scores


def score_observations(observations: Sequence[Observation]) -> list[dict[str, object]]:
    by_fuel: dict[str, list[Observation]] = defaultdict(list)
    for observation in observations:
        by_fuel[observation.fuel].append(observation)

    rows: list[dict[str, object]] = []
    for fuel, fuel_observations in by_fuel.items():
        price_scores = _percentile_scores(
            fuel_observations,
            lambda row: row.noon_price,
            higher_is_better=False,
        )
        stability_scores = _percentile_scores(
            fuel_observations,
            lambda row: row.span_cents,
            higher_is_better=False,
        )
        first_drop_scores = _percentile_scores(
            fuel_observations,
            lambda row: row.first_markdown_score_value,
            higher_is_better=False,
        )
        early_markdown_scores = _percentile_scores(
            fuel_observations,
            lambda row: row.markdown_by_18_cents,
            higher_is_better=True,
        )

        for observation in fuel_observations:
            key = observation.key
            price_score = price_scores[key]
            stability_score = stability_scores[key]
            markdown_speed_score = (
                (0.6 * first_drop_scores[key])
                + (0.4 * early_markdown_scores[key])
            )
            customer_score = (
                price_score + stability_score + markdown_speed_score
            ) / 3.0
            rows.append(
                {
                    "station_uuid": observation.station_uuid,
                    "fuel": fuel,
                    "fuel_label": FUEL_LABELS.get(fuel, fuel),
                    "noon_price": observation.noon_price,
                    "span_cents": observation.span_cents,
                    "first_markdown_hour": observation.first_markdown_hour,
                    "first_markdown_score_value": observation.first_markdown_score_value,
                    "markdown_by_14_cents": observation.markdown_by_14_cents,
                    "markdown_by_16_cents": observation.markdown_by_16_cents,
                    "markdown_by_18_cents": observation.markdown_by_18_cents,
                    "markdown_by_22_cents": observation.markdown_by_22_cents,
                    "cycle_days": observation.cycle_days,
                    "price_level_score": price_score,
                    "stability_score": stability_score,
                    "markdown_speed_score": round(markdown_speed_score, 3),
                    "customer_friendliness_score": round(customer_score, 3),
                }
            )
    return sorted(
        rows,
        key=lambda row: (
            -float(row["customer_friendliness_score"]),
            -float(row["price_level_score"]),
            str(row["station_uuid"]),
            str(row["fuel"]),
        ),
    )


def _ranked(rows: list[dict[str, object]], score_key: str) -> list[dict[str, object]]:
    ranked: list[dict[str, object]] = []
    last_score: float | None = None
    last_rank = 0
    for index, row in enumerate(rows, start=1):
        score = round(float(row[score_key]), 6)
        if last_score is None or score != last_score:
            last_rank = index
            last_score = score
        ranked.append({"rank": last_rank, **row})
    return ranked


def build_station_rows(
    scored_fuel_rows: Sequence[dict[str, object]],
    stations: dict[str, Station],
    *,
    min_fuels: int,
) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in scored_fuel_rows:
        grouped[str(row["station_uuid"])].append(row)

    station_rows: list[dict[str, object]] = []
    for station_uuid, fuel_rows in grouped.items():
        fuels = sorted({str(row["fuel"]) for row in fuel_rows})
        if len(fuels) < min_fuels:
            continue
        station = stations.get(station_uuid)
        if station is None:
            continue

        first_hours = [
            float(row["first_markdown_score_value"])
            for row in fuel_rows
            if float(row["first_markdown_score_value"]) < NO_MARKDOWN_SENTINEL_HOUR
        ]
        station_rows.append(
            {
                "station_uuid": station_uuid,
                "name": station.name,
                "brand": station.brand,
                "city": station.city,
                "post_code": station.post_code,
                "street": station.street,
                "house_number": station.house_number,
                "fuels": "|".join(fuels),
                "fuel_count": len(fuels),
                "customer_friendliness_score": round(
                    _mean(float(row["customer_friendliness_score"]) for row in fuel_rows),
                    3,
                ),
                "price_level_score": round(
                    _mean(float(row["price_level_score"]) for row in fuel_rows), 3
                ),
                "stability_score": round(
                    _mean(float(row["stability_score"]) for row in fuel_rows), 3
                ),
                "markdown_speed_score": round(
                    _mean(float(row["markdown_speed_score"]) for row in fuel_rows), 3
                ),
                "avg_noon_price_eur_l": round(
                    _mean(float(row["noon_price"]) for row in fuel_rows), 3
                ),
                "avg_span_cents": round(
                    _mean(float(row["span_cents"]) for row in fuel_rows), 2
                ),
                "median_first_markdown_hour_after_12": (
                    round(statistics.median(first_hours), 1) if first_hours else None
                ),
                "avg_markdown_by_16_cents": round(
                    _mean(float(row["markdown_by_16_cents"]) for row in fuel_rows), 2
                ),
                "avg_markdown_by_18_cents": round(
                    _mean(float(row["markdown_by_18_cents"]) for row in fuel_rows), 2
                ),
                "avg_markdown_by_22_cents": round(
                    _mean(float(row["markdown_by_22_cents"]) for row in fuel_rows), 2
                ),
                "min_cycle_days": min(int(row["cycle_days"]) for row in fuel_rows),
            }
        )

    station_rows = sorted(
        station_rows,
        key=lambda row: (
            -float(row["customer_friendliness_score"]),
            -float(row["price_level_score"]),
            str(row["station_uuid"]),
        ),
    )
    return _ranked(station_rows, "customer_friendliness_score")


def build_station_fuel_rows(
    scored_fuel_rows: Sequence[dict[str, object]],
    stations: dict[str, Station],
) -> list[dict[str, object]]:
    enriched: list[dict[str, object]] = []
    for row in scored_fuel_rows:
        station = stations.get(str(row["station_uuid"]))
        if station is None:
            continue
        enriched.append(
            {
                "station_uuid": row["station_uuid"],
                "name": station.name,
                "brand": station.brand,
                "city": station.city,
                "post_code": station.post_code,
                "fuel": row["fuel"],
                "fuel_label": row["fuel_label"],
                "customer_friendliness_score": row["customer_friendliness_score"],
                "price_level_score": row["price_level_score"],
                "stability_score": row["stability_score"],
                "markdown_speed_score": row["markdown_speed_score"],
                "noon_price_eur_l": round(float(row["noon_price"]), 3),
                "span_cents": round(float(row["span_cents"]), 2),
                "first_markdown_hour_after_12": row["first_markdown_hour"],
                "markdown_by_14_cents": round(float(row["markdown_by_14_cents"]), 2),
                "markdown_by_16_cents": round(float(row["markdown_by_16_cents"]), 2),
                "markdown_by_18_cents": round(float(row["markdown_by_18_cents"]), 2),
                "markdown_by_22_cents": round(float(row["markdown_by_22_cents"]), 2),
                "cycle_days": row["cycle_days"],
            }
        )
    enriched = sorted(
        enriched,
        key=lambda row: (
            -float(row["customer_friendliness_score"]),
            -float(row["price_level_score"]),
            str(row["station_uuid"]),
            str(row["fuel"]),
        ),
    )
    return _ranked(enriched, "customer_friendliness_score")


def build_brand_rows(
    station_rows: Sequence[dict[str, object]],
    *,
    min_stations: int,
) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in station_rows:
        grouped[str(row["brand"])].append(row)

    brand_rows: list[dict[str, object]] = []
    for brand, rows in grouped.items():
        if len(rows) < min_stations:
            continue
        brand_rows.append(
            {
                "brand": brand,
                "station_count": len(rows),
                "customer_friendliness_score": round(
                    _mean(float(row["customer_friendliness_score"]) for row in rows),
                    3,
                ),
                "price_level_score": round(
                    _mean(float(row["price_level_score"]) for row in rows), 3
                ),
                "stability_score": round(
                    _mean(float(row["stability_score"]) for row in rows), 3
                ),
                "markdown_speed_score": round(
                    _mean(float(row["markdown_speed_score"]) for row in rows), 3
                ),
                "avg_span_cents": round(
                    _mean(float(row["avg_span_cents"]) for row in rows), 2
                ),
                "avg_markdown_by_18_cents": round(
                    _mean(float(row["avg_markdown_by_18_cents"]) for row in rows), 2
                ),
            }
        )

    brand_rows = sorted(
        brand_rows,
        key=lambda row: (
            -float(row["customer_friendliness_score"]),
            -int(row["station_count"]),
            str(row["brand"]),
        ),
    )
    return _ranked(brand_rows, "customer_friendliness_score")


def assign_awards(station_rows: Sequence[dict[str, object]]) -> list[dict[str, object]]:
    station_count = len(station_rows)
    thresholds = {
        tier: max(1, math.ceil(station_count * share))
        for tier, _, share in AWARD_TIERS
    }
    awarded_rows: list[dict[str, object]] = []
    for row in station_rows:
        rank = int(row["rank"])
        award_tier = ""
        award_label = ""
        award_top_percent: float | None = None
        for tier, label, share in AWARD_TIERS:
            if rank <= thresholds[tier]:
                award_tier = tier
                award_label = label
                award_top_percent = share * 100
                break
        enriched = dict(row)
        enriched["award_tier"] = award_tier
        enriched["award_label"] = award_label
        enriched["award_top_percent"] = award_top_percent or ""
        awarded_rows.append(enriched)
    return awarded_rows


def write_awards_json(
    path: Path,
    station_rows: Sequence[dict[str, object]],
    *,
    noon_snapshot: NoonSnapshot,
) -> None:
    station_count = len(station_rows)
    thresholds = {
        tier: {
            "label": label,
            "top_percent": share * 100,
            "rank_threshold": max(1, math.ceil(station_count * share)),
        }
        for tier, label, share in AWARD_TIERS
    }
    awards: dict[str, dict[str, object]] = {}
    counts = {tier: 0 for tier, _, _ in AWARD_TIERS}
    for row in station_rows:
        tier = str(row.get("award_tier") or "")
        if not tier:
            continue
        counts[tier] += 1
        station_uuid = str(row["station_uuid"])
        awards[station_uuid] = {
            "tier": tier,
            "label": row["award_label"],
            "rank": int(row["rank"]),
            "score": float(row["customer_friendliness_score"]),
            "top_percent": float(row["award_top_percent"]),
        }

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "noon_snapshot": noon_snapshot.latest_update,
        "station_count": station_count,
        "criteria": [
            "Preisniveau",
            "Preisstabilitaet",
            "Senkungsgeschwindigkeit nach 12 Uhr",
        ],
        "thresholds": thresholds,
        "award_counts": counts,
        "awards": awards,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_csv(path: Path, rows: Sequence[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _markdown_table(rows: Sequence[dict[str, object]], columns: Sequence[tuple[str, str]], limit: int) -> list[str]:
    selected = list(rows[:limit])
    lines = [
        "| " + " | ".join(header for header, _ in columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in selected:
        values: list[str] = []
        for _, key in columns:
            value = row.get(key)
            if isinstance(value, float):
                digits = 1 if ("score" in key or "cents" in key or "hour" in key) else 3
                values.append(_fmt(value, digits))
            elif value is None:
                values.append("keine")
            else:
                values.append(str(value))
        lines.append("| " + " | ".join(values) + " |")
    return lines


def write_report(
    path: Path,
    *,
    station_rows: Sequence[dict[str, object]],
    station_fuel_rows: Sequence[dict[str, object]],
    brand_rows: Sequence[dict[str, object]],
    noon_snapshot: NoonSnapshot,
    observation_count: int,
    min_station_fuels: int,
    min_brand_stations: int,
    outputs: OutputPaths,
) -> None:
    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines: list[str] = [
        "# Kundenfreundlichste Tankstellen",
        "",
        f"Erzeugt: {generated_at}",
        f"Mittags-Snapshot: {noon_snapshot.latest_update or 'unbekannt'}",
        "",
        "## Kurzfazit",
        "",
        (
            f"Ausgewertet wurden {observation_count:,} Station-Kraftstoff-Kombinationen "
            f"und {len(station_rows):,} Tankstellen mit mindestens {min_station_fuels} auswertbaren Kraftstoffen."
        ).replace(",", "."),
        "Der Score ist ein gleich gewichteter Index aus Preisniveau, Preisstabilitaet und Senkungsgeschwindigkeit nach 12 Uhr.",
        "",
        "## Methodik",
        "",
        "- Preisniveau: niedriger 12:00-Referenzpreis innerhalb des jeweiligen Kraftstoffs ist besser.",
        "- Preisstabilitaet: kleinere untertaegige Preisspanne (`span`) ist besser.",
        "- Senkungsgeschwindigkeit: frueher erste Senkung nach 12 Uhr und hoehere Senkung bis 18 Uhr sind besser.",
        "- Alle Teilwerte werden pro Kraftstoff als Perzentilscore von 0 bis 100 berechnet; 100 ist kundenfreundlicher.",
        "- Die Gesamtwertung einer Tankstelle ist der Mittelwert ihrer auswertbaren Kraftstoffe.",
        "- Auszeichnungen: Top 2 Prozent = Gold, Top 5 Prozent = Silber, Top 10 Prozent = Bronze.",
        "",
        "## Top-Tankstellen",
        "",
    ]
    lines.extend(
        _markdown_table(
            station_rows,
            (
                ("Rang", "rank"),
                ("Tankstelle", "name"),
                ("Marke", "brand"),
                ("Ort", "city"),
                ("Score", "customer_friendliness_score"),
                ("Preis", "price_level_score"),
                ("Stabil", "stability_score"),
                ("Senkung", "markdown_speed_score"),
                ("Auszeichnung", "award_label"),
                ("erste Senkung h", "median_first_markdown_hour_after_12"),
                ("Senkung 18h ct", "avg_markdown_by_18_cents"),
            ),
            20,
        )
    )
    lines.extend(["", "## Top-Marken", ""])
    if brand_rows:
        lines.extend(
            _markdown_table(
                brand_rows,
                (
                    ("Rang", "rank"),
                    ("Marke", "brand"),
                    ("Stationen", "station_count"),
                    ("Score", "customer_friendliness_score"),
                    ("Preis", "price_level_score"),
                    ("Stabil", "stability_score"),
                    ("Senkung", "markdown_speed_score"),
                ),
                15,
            )
        )
    else:
        lines.append(
            f"Keine Marke erreicht die Mindeststichprobe von {min_brand_stations} Tankstellen."
        )
    lines.extend(
        [
            "",
            "## Staerkste Station-Kraftstoff-Kombinationen",
            "",
        ]
    )
    lines.extend(
        _markdown_table(
            station_fuel_rows,
            (
                ("Rang", "rank"),
                ("Kraftstoff", "fuel_label"),
                ("Tankstelle", "name"),
                ("Marke", "brand"),
                ("Ort", "city"),
                ("Score", "customer_friendliness_score"),
                ("12 Uhr EUR/l", "noon_price_eur_l"),
                ("Spanne ct", "span_cents"),
                ("erste Senkung h", "first_markdown_hour_after_12"),
                ("Senkung 18h ct", "markdown_by_18_cents"),
            ),
            20,
        )
    )
    lines.extend(
        [
            "",
            "## Einordnung",
            "",
            "Diese Auswertung ist bewusst verbraucherorientiert. Sie bewertet nicht, ob ein Preis betriebswirtschaftlich sinnvoll ist, sondern ob die beobachtete Preisfuehrung fuer Kundinnen und Kunden angenehm ist: niedrig, ruhig und nach dem Mittagsreset zuegig fallend.",
            "",
            "## Dateien",
            "",
            f"- Station-Ranking: `{outputs.station_csv}`",
            f"- Station-Kraftstoff-Ranking: `{outputs.station_fuel_csv}`",
            f"- Marken-Ranking: `{outputs.brand_csv}`",
            f"- Report: `{outputs.report_md}`",
            f"- Website-Auszeichnungen: `{outputs.awards_json}`",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate(
    *,
    stations_path: Path = ROOT / "data" / "stations.json",
    data2_dir: Path = ROOT / "data2",
    noon_csv: Path = ROOT / "data" / "noon.csv",
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    awards_json: Path = DEFAULT_AWARDS_PATH,
    min_station_fuels: int = 2,
    min_brand_stations: int = 20,
) -> OutputPaths:
    stations = load_stations(stations_path)
    noon_snapshot = load_noon_snapshot(noon_csv)
    observations = load_observations(data2_dir, noon_snapshot, stations)
    if not observations:
        raise SystemExit("No usable customer-friendliness observations found.")

    scored_fuel_rows = score_observations(observations)
    station_fuel_rows = build_station_fuel_rows(scored_fuel_rows, stations)
    station_rows = build_station_rows(
        scored_fuel_rows,
        stations,
        min_fuels=min_station_fuels,
    )
    station_rows = assign_awards(station_rows)
    brand_rows = build_brand_rows(station_rows, min_stations=min_brand_stations)

    outputs = OutputPaths(
        station_csv=output_dir / "station_customer_friendliness.csv",
        station_fuel_csv=output_dir / "station_fuel_customer_friendliness.csv",
        brand_csv=output_dir / "brand_customer_friendliness.csv",
        report_md=output_dir / "customer_friendliness_report.md",
        awards_json=awards_json,
    )
    _write_csv(outputs.station_csv, station_rows)
    _write_csv(outputs.station_fuel_csv, station_fuel_rows)
    _write_csv(outputs.brand_csv, brand_rows)
    write_awards_json(outputs.awards_json, station_rows, noon_snapshot=noon_snapshot)
    write_report(
        outputs.report_md,
        station_rows=station_rows,
        station_fuel_rows=station_fuel_rows,
        brand_rows=brand_rows,
        noon_snapshot=noon_snapshot,
        observation_count=len(observations),
        min_station_fuels=min_station_fuels,
        min_brand_stations=min_brand_stations,
        outputs=outputs,
    )
    return outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stations-json", type=Path, default=ROOT / "data" / "stations.json")
    parser.add_argument("--data2-dir", type=Path, default=ROOT / "data2")
    parser.add_argument("--noon-csv", type=Path, default=ROOT / "data" / "noon.csv")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--awards-json", type=Path, default=DEFAULT_AWARDS_PATH)
    parser.add_argument(
        "--min-station-fuels",
        type=int,
        default=2,
        help="Minimum number of usable fuels required for the station-level ranking.",
    )
    parser.add_argument(
        "--min-brand-stations",
        type=int,
        default=20,
        help="Minimum station count required for the brand-level ranking.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    outputs = generate(
        stations_path=args.stations_json,
        data2_dir=args.data2_dir,
        noon_csv=args.noon_csv,
        output_dir=args.output_dir,
        awards_json=args.awards_json,
        min_station_fuels=max(1, args.min_station_fuels),
        min_brand_stations=max(1, args.min_brand_stations),
    )
    print(f"Wrote {outputs.station_csv}")
    print(f"Wrote {outputs.station_fuel_csv}")
    print(f"Wrote {outputs.brand_csv}")
    print(f"Wrote {outputs.report_md}")
    print(f"Wrote {outputs.awards_json}")


if __name__ == "__main__":
    main()
