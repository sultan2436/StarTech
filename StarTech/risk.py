from predict import hybrid_spread

def add_risk_priority(data):
    HUMAN_MAP = {
        "urban": 0.8,
        "tourism": 1.0,
        "village": 0.5,
        "forest": 0.2
    }

    for p in data:
        result = hybrid_spread(p)

        p["base_spread"] = result["base"]
        p["ml_spread"] = result["ml"]
        p["spread_rate"] = result["final"]

        p["risk"] = (
            p["spread_rate"] * 0.5 +
            p["wind"] * 0.2 +
            (100 - p["humidity"]) * 0.2 +
            p.get("slope_risk", 0) * 0.1
        )

        human = HUMAN_MAP.get(p["poi_type"], 0.3)
        p["risk"] += human * 5

        p["priority"] = (
            (1 if p["poi_type"] == "hospital"
             else 0.8 if p["poi_type"] == "school"
             else 0.6)
            + p["risk"] * 0.3
        )

    return data