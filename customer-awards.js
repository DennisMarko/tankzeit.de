(function () {
  const AWARDS_URL = "data/customer_friendliness_awards.json?v=20260504-awards";
  const ALLOWED_TIERS = new Set(["gold", "silver", "bronze"]);
  let awardsPromise = null;
  let awardMap = {};

  function escapeHtml(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }

  async function loadAwards() {
    if (!awardsPromise) {
      awardsPromise = fetch(AWARDS_URL)
        .then((response) => {
          if (!response.ok) {
            return {};
          }
          return response.json();
        })
        .then((payload) => {
          awardMap = payload?.awards || {};
          return awardMap;
        })
        .catch(() => {
          awardMap = {};
          return awardMap;
        });
    }
    return awardsPromise;
  }

  function awardForStation(stationId) {
    const award = awardMap?.[stationId];
    if (!award || typeof award !== "object") {
      return null;
    }
    const tier = String(award.tier || "").toLowerCase();
    if (!ALLOWED_TIERS.has(tier)) {
      return null;
    }
    return {
      tier,
      label: String(award.label || tier).trim(),
      rank: Number(award.rank) || null,
      score: Number(award.score) || null,
    };
  }

  function badgeHtml(award) {
    if (!award) {
      return "";
    }
    const label = award.label || award.tier;
    return `
      <span class="station-award station-award--${award.tier}" aria-label="Auszeichnung ${escapeHtml(label)}">
        <span class="station-award-star" aria-hidden="true">&#9733;</span>
        <span>${escapeHtml(label)}</span>
      </span>
    `;
  }

  function badgeForStation(stationId) {
    return badgeHtml(awardForStation(stationId));
  }

  window.TankzeitCustomerAwards = {
    awardForStation,
    badgeForStation,
    badgeHtml,
    loadAwards,
  };
})();
