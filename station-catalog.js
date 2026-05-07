(function () {
  const STATIONS_URL = "data/stations.json";
  let stationCatalogPromise = null;

  function toFiniteNumber(value) {
    const numericValue = Number(value);
    return Number.isFinite(numericValue) ? numericValue : null;
  }

  function isSupportedCoordinate(lat, lng) {
    return lat >= 47 && lat <= 56 && lng >= 5 && lng <= 16;
  }

  function isTestStation(station) {
    const name = String(station?.name || "").trim().toLowerCase();
    const brand = String(station?.brand || "").trim().toLowerCase();
    const city = String(station?.city || "").trim().toLowerCase();
    const uuid = String(station?.uuid || "").trim().toLowerCase();
    const explicitTestIds = new Set([
      "4e8ecfc5-5d0d-4463-901b-6b9ff8fee510",
      "ef278d2c-8d50-4191-b2d2-e4a2d4dd2fdf",
      "ce830342-ebca-4bf8-9593-653341732a59",
      "00099999-751a-4444-8888-acdc00000001",
    ]);

    return (
      explicitTestIds.has(uuid) ||
      name === "01_test" ||
      name === "test (mdm)" ||
      name.includes("testkasse") ||
      name.includes("mustermann") ||
      city.includes("testkasse") ||
      brand === "test"
    );
  }

  function haversineDistanceKm(lat1, lng1, lat2, lng2) {
    const earthRadiusKm = 6371;
    const toRadians = (value) => (value * Math.PI) / 180;
    const dLat = toRadians(lat2 - lat1);
    const dLng = toRadians(lng2 - lng1);
    const a =
      Math.sin(dLat / 2) ** 2 +
      Math.cos(toRadians(lat1)) *
        Math.cos(toRadians(lat2)) *
        Math.sin(dLng / 2) ** 2;
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return earthRadiusKm * c;
  }

  async function loadCatalog() {
    if (!stationCatalogPromise) {
      stationCatalogPromise = fetch(STATIONS_URL).then((response) => {
        if (!response.ok) {
          throw new Error(`Request failed: ${response.status}`);
        }
        return response.json();
      });
    }
    return stationCatalogPromise;
  }

  function findNearbyStations(stations, lat, lng, options = {}) {
    const limit = Number.isFinite(options.limit) ? options.limit : 10;
    const radiusKm = Number.isFinite(options.radiusKm) ? options.radiusKm : 10;
    const centerLat = toFiniteNumber(lat);
    const centerLng = toFiniteNumber(lng);

    if (
      !Number.isFinite(centerLat) ||
      !Number.isFinite(centerLng) ||
      !isSupportedCoordinate(centerLat, centerLng)
    ) {
      return [];
    }

    return (stations || [])
      .map((station) => {
        const stationLat = toFiniteNumber(station.latitude);
        const stationLng = toFiniteNumber(station.longitude);
        if (
          !Number.isFinite(stationLat) ||
          !Number.isFinite(stationLng) ||
          !isSupportedCoordinate(stationLat, stationLng) ||
          isTestStation(station)
        ) {
          return null;
        }

        return {
          id: station.uuid,
          name: station.name || station.brand || "Tankstelle",
          brand: station.brand || "",
          lat: stationLat,
          lng: stationLng,
          dist: haversineDistanceKm(centerLat, centerLng, stationLat, stationLng),
        };
      })
      .filter(Boolean)
      .filter((station) => station.dist <= radiusKm)
      .sort((left, right) => {
        if (left.dist !== right.dist) return left.dist - right.dist;
        return `${left.name} ${left.brand}`.localeCompare(
          `${right.name} ${right.brand}`,
          "de",
          { sensitivity: "base" },
        );
      })
      .slice(0, limit);
  }

  window.TankzeitStationCatalog = {
    findNearbyStations,
    loadCatalog,
  };
})();
