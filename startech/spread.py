import math


# 🔥 1. YÖN SKORU (rüzgar yönü etkisi)
def calculate_direction_score(src, target, wind_dir):
    """
    wind_dir: derece (0 = kuzey, 90 = doğu)
    """

    dx = target["lon"] - src["lon"]
    dy = target["lat"] - src["lat"]

    angle = math.degrees(math.atan2(dx, dy)) % 360

    diff = abs(angle - wind_dir)
    diff = min(diff, 360 - diff)

    # aynı yön = 1.0, ters yön = 0
    score = max(0, 1 - diff / 180)

    return score


# 🔥 2. MESAFE
def calculate_distance(src, target):
    dx = src["lat"] - target["lat"]
    dy = src["lon"] - target["lon"]

    return math.sqrt(dx * dx + dy * dy)


# 🔥 3. YAYILMA OLASILIĞI
def spread_probability(src, target):
    wind_dir = src.get("wind_dir", 90)  # default doğu

    direction_score = calculate_direction_score(src, target, wind_dir)
    distance = calculate_distance(src, target)

    if distance == 0:
        return 0

    distance_score = 1 / distance

    # topoğrafya (opsiyonel)
    slope_effect = target.get("slope", 0) * 0.1

    # 🔥 ANA FORMÜL
    probability = (
        direction_score * 0.5 +
        distance_score * 0.25 +
        target["risk"] * 0.2 +
        slope_effect
    )

    return probability


# 🔥 4. YANGIN YAYILIM SİMÜLASYONU
def simulate_fire_spread(points, threshold=0.6):
    edges = []

    for src in points:
        for target in points:
            if src == target:
                continue

            prob = spread_probability(src, target)

            if prob > threshold:
                edges.append({
                    "from": src["name"],
                    "to": target["name"],
                    "prob": round(prob, 2),
                    "wind_dir": src.get("wind_dir", 90)
                })

    return edges