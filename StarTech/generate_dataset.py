import json
import random

with open("mugla_data.json") as f:
    data = json.load(f)


def base_spread(p):
    veg_factor = {
        "kizilcam": 1.0,
        "maki": 0.8,
        "mesek": 0.4,
        "urban": 0.1,
        "zeytin": 0.5
    }.get(p.get("vegetation", "urban"), 0.5)

    return (
        p["wind"] * 0.4 +
        (100 - p["humidity"]) * 0.3 +
        p.get("slope_deg", p.get("slope_risk", 0)) * 0.2 +
        p["temperature"] * 0.2 +
        veg_factor * 20
    )


dataset = []

for p in data:
    # 🔥 eksik verileri üret
    wind = random.randint(10, 50)
    humidity = random.randint(10, 90)
    temperature = random.randint(20, 45)
    slope = random.randint(0, 30)

    fake_point = {
        "wind": wind,
        "humidity": humidity,
        "temperature": temperature,
        "vegetation": random.choice(["kizilcam", "maki", "mesek"]),
        "slope_risk": slope
    }

    spread = base_spread(fake_point)

    dataset.append({
        "wind": wind,
        "humidity": humidity,
        "temperature": temperature,
        "vegetation": fake_point["vegetation"],
        "slope": slope,
        "spread_rate": spread
    })


with open("dataset.json", "w") as f:
    json.dump(dataset, f, indent=2)

print("dataset.json oluşturuldu 🚀")