from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from data import get_dataset, get_roads
from risk import add_risk_priority
from route import simple_route
from spread import simulate_fire_spread


# 🔥 ÖNCE APP TANIMLANIR
app = FastAPI()

# 🌐 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🏠 ANA ENDPOINT
@app.get("/")
def home():
    return {"message": "Disaster Response System Running"}


# 🔥 RISK MAP
@app.get("/risk-map")
def risk_map():
    data = get_dataset()
    data = add_risk_priority(data)

    return [
        {
            "name": p["name"],
            "lat": p["lat"],
            "lon": p["lon"],
            "risk": round(p["risk"], 2),
            "spread": round(p["spread_rate"], 2),
            "base_spread": round(p["base_spread"], 2),
            "ml_spread": round(p["ml_spread"], 2),
            "poi_type": p["poi_type"]
        }
        for p in data
    ]


# 🛣️ ROTA
@app.get("/route")
def get_route():
    raw = get_dataset()
    processed = add_risk_priority(raw)
    roads = get_roads()

    return simple_route(processed, roads)


# 🛣️ YOLLAR
@app.get("/roads")
def roads():
    return get_roads()


# 🔥 YANGIN YAYILIMI (EN SONA KOY)
@app.get("/spread")
def spread():
    data = get_dataset()
    data = add_risk_priority(data)

    return simulate_fire_spread(data)