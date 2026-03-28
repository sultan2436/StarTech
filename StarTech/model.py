from sklearn.ensemble import RandomForestRegressor
import json
import joblib

# 📦 DATASET YÜKLE
with open("dataset.json") as f:
    data = json.load(f)

X = []
y = []

veg_map = {
    "kizilcam": 1.0,
    "maki": 0.9,
    "mesek": 0.4,
    "urban": 0.1
}

for d in data:
    X.append([
        d["wind"],
        d["humidity"],
        d["temperature"],
        veg_map.get(d["vegetation"], 0.5),
        d.get("slope_risk", 0)
    ])
    y.append(d["spread_rate"])


# 🤖 MODEL
model = RandomForestRegressor()
model.fit(X, y)

# 💾 KAYDET
joblib.dump(model, "fire_model.pkl")

print("Model eğitildi 🚀")