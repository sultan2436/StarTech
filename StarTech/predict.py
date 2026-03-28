import joblib

# model yükle
model = joblib.load("fire_model.pkl")

VEG_MAP = {
    "kizilcam": 1.0,
    "maki": 0.8,
    "mesek": 0.4,
    "urban": 0.1,
    "zeytin": 0.5
}

# 🔥 KURAL MODEL
def base_spread(p):
    veg_factor = VEG_MAP.get(p["vegetation"], 0.5)

    wind_effect = p["wind"] * 0.4
    humidity_effect = (100 - p["humidity"]) * 0.3
    slope_effect = p.get("slope_risk", 0) * 0.2
    temp_effect = p["temperature"] * 0.2

    return wind_effect + humidity_effect + slope_effect + temp_effect + (veg_factor * 20)


# 🤖 ML MODEL
def ml_spread(p):
    X = [[
        p["wind"],
        p["humidity"],
        p["temperature"],
        VEG_MAP.get(p["vegetation"], 0.5),
        p.get("slope_risk", 0)
    ]]
    return float(model.predict(X)[0])


# ⚡ HYBRID MODEL
def hybrid_spread(p):
    base = base_spread(p)
    ml = ml_spread(p)

    final = 0.7 * base + 0.3 * ml

    return {
        "base": base,
        "ml": ml,
        "final": final
    }