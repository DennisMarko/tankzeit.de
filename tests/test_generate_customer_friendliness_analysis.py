import csv
import json
import shutil
import unittest
from pathlib import Path

from scripts.generate_customer_friendliness_analysis import (
    _cycle_rows_by_hour,
    _first_markdown_hour,
    generate,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def _station_path(data2_dir: Path, station_uuid: str) -> Path:
    first, second, third, fourth, fifth = station_uuid.split("-")
    return data2_dir / first / second / third / fourth / fifth


def _write_payload(
    data2_dir: Path,
    station_uuid: str,
    *,
    span: float,
    markdown_by_hour: dict[int, float],
) -> None:
    rows = []
    for cycle_hour in range(0, 11):
        markdown = markdown_by_hour.get(cycle_hour, 0.0)
        rows.append(
            {
                "cycle_hour": cycle_hour,
                "clock_hour": (12 + cycle_hour) % 24,
                "markdown_median": markdown,
                "delta_median": -markdown,
            }
        )
    path = _station_path(data2_dir, station_uuid)
    path.mkdir(parents=True, exist_ok=True)
    (path / "diesel.json").write_text(
        json.dumps(
            {
                "span": span,
                "cycle_hourly": rows,
                "cycle_summary": {"days": 2},
            }
        ),
        encoding="utf-8",
    )


class CustomerFriendlinessAnalysisTests(unittest.TestCase):
    def test_first_markdown_hour_uses_half_cent_threshold(self) -> None:
        rows_by_hour = _cycle_rows_by_hour(
            {
                "cycle_hourly": [
                    {"cycle_hour": 0, "markdown_median": 0.0},
                    {"cycle_hour": 1, "markdown_median": 0.004},
                    {"cycle_hour": 2, "markdown_median": 0.006},
                ]
            }
        )

        self.assertEqual(_first_markdown_hour(rows_by_hour), 2.0)

    def test_generate_ranks_low_stable_fast_station_first(self) -> None:
        station_fast = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        station_mid = "bbbbbbbb-cccc-dddd-eeee-ffffffffffff"
        station_slow = "cccccccc-dddd-eeee-ffff-000000000000"

        root = REPO_ROOT / "tmp_customer_friendliness_test"
        if root.exists():
            shutil.rmtree(root)
        root.mkdir()
        try:
            data_dir = root / "data"
            data2_dir = root / "data2"
            output_dir = root / "output"
            data_dir.mkdir()
            stations_path = data_dir / "stations.json"
            noon_path = data_dir / "noon.csv"

            stations_path.write_text(
                json.dumps(
                    [
                        {
                            "uuid": station_fast,
                            "name": "Fast",
                            "brand": "FairFuel",
                            "city": "A",
                        },
                        {
                            "uuid": station_mid,
                            "name": "Middle",
                            "brand": "FairFuel",
                            "city": "B",
                        },
                        {
                            "uuid": station_slow,
                            "name": "Slow",
                            "brand": "SlowFuel",
                            "city": "C",
                        },
                    ]
                ),
                encoding="utf-8",
            )
            noon_path.write_text(
                "\n".join(
                    [
                        "station_uuid,diesel,last_update",
                        f"{station_fast},1.60,2026-04-23T12:00:00+02:00",
                        f"{station_mid},1.70,2026-04-23T12:00:00+02:00",
                        f"{station_slow},1.90,2026-04-23T12:00:00+02:00",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            _write_payload(
                data2_dir,
                station_fast,
                span=0.02,
                markdown_by_hour={1: 0.01, 6: 0.04, 10: 0.07},
            )
            _write_payload(
                data2_dir,
                station_mid,
                span=0.05,
                markdown_by_hour={3: 0.01, 6: 0.02, 10: 0.04},
            )
            _write_payload(
                data2_dir,
                station_slow,
                span=0.11,
                markdown_by_hour={10: 0.01},
            )

            outputs = generate(
                stations_path=stations_path,
                data2_dir=data2_dir,
                noon_csv=noon_path,
                output_dir=output_dir,
                awards_json=data_dir / "customer_friendliness_awards.json",
                min_station_fuels=1,
                min_brand_stations=1,
            )

            with outputs.station_csv.open("r", encoding="utf-8", newline="") as handle:
                station_rows = list(csv.DictReader(handle))
            self.assertEqual(station_rows[0]["station_uuid"], station_fast)
            self.assertEqual(station_rows[0]["rank"], "1")

            report = outputs.report_md.read_text(encoding="utf-8")
            self.assertIn("Kundenfreundlichste Tankstellen", report)
            self.assertIn("Auszeichnungen: Top 2 Prozent = Gold", report)
            self.assertNotIn("lokale Fairness", report)

            awards = json.loads(outputs.awards_json.read_text(encoding="utf-8"))
            self.assertEqual(awards["awards"][station_fast]["tier"], "gold")
        finally:
            shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
