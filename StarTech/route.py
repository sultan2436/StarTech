import math

def distance(p1, p2):
    return math.sqrt((p1["lat"] - p2["lat"])**2 + (p1["lon"] - p2["lon"])**2)

def find_road_safety(lat, lon, roads):
    if not roads:
        return 0.5
    best = min(
        roads,
        key=lambda r: min(
            (abs(g.get("lat", 0) - lat) + abs(g.get("lon", 0) - lon))
            for g in r["geometry"]
        ) if r["geometry"] else 999
    )
    return best["safety"]

def simple_route(data, roads=None):
    if not data:
        return []

    roads = roads or []
    start = max(data, key=lambda x: x["priority"] + x["risk"])
    visited = [start]
    remaining = [p for p in data if p != start]

    while remaining:
        current = visited[-1]
        road_safety = find_road_safety(current["lat"], current["lon"], roads)
        best = max(
            remaining,
            key=lambda p: (
                p["priority"] - p["risk"]
                - distance(current, p) * 2
                + road_safety * 0.3
            )
        )
        visited.append(best)
        remaining.remove(best)

    return [
        {
            "lat":      p["lat"],
            "lon":      p["lon"],
            "risk":     p["risk"],
            "priority": p["priority"],
            "poi_type": p["poi_type"],
            "order":    i + 1
        }
        for i, p in enumerate(visited[:8])
    ]