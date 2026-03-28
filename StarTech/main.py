from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from data import get_dataset, get_roads
from risk import add_risk_priority
from route import simple_route
from spread import simulate_fire_spread

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔁 Basit in-memory cache
_cache = {"data": None, "roads": None}

def get_processed_data():
    if _cache["data"] is None:
        raw = get_dataset()
        _cache["data"] = add_risk_priority(raw)
    return _cache["data"]

def get_cached_roads():
    if _cache["roads"] is None:
        _cache["roads"] = get_roads()
    return _cache["roads"]


@app.get("/")
def home():
    return {"message": "Disaster Response System Running"}


@app.get("/risk-map")
def risk_map():
    try:
        data = get_processed_data()
        return [
            {
                "name":        p["name"],
                "lat":         p["lat"],
                "lon":         p["lon"],
                "poi_type":    p["poi_type"],
                "vegetation":  p["vegetation"],
                "risk":        round(p["risk"], 2),
                "spread":      round(p["spread_rate"], 2),
                "base_spread": round(p["base_spread"], 2),
                "ml_spread":   round(p["ml_spread"], 2),
                "wind":        round(p["wind"], 2),
                "humidity":    round(p["humidity"], 2),
                "temperature": round(p["temperature"], 2),
                "elevation":   round(p.get("elevation", 0), 1),
                "slope_deg":   round(p.get("slope_deg", 0), 2),
                "slope_risk":  round(p.get("slope_risk", 0), 3),
            }
            for p in data
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Risk haritası hatası: {str(e)}")


@app.get("/route")
def get_route():
    try:
        data  = get_processed_data()
        roads = get_cached_roads()
        return simple_route(data, roads)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rota hatası: {str(e)}")


@app.get("/roads")
def roads():
    try:
        return get_cached_roads()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Yol verisi hatası: {str(e)}")


@app.get("/spread")
def spread():
    try:
        data = get_processed_data()
        return simulate_fire_spread(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Yayılım hatası: {str(e)}")


@app.post("/cache/clear")
def clear_cache():
    _cache["data"]  = None
    _cache["roads"] = None
    return {"message": "Cache temizlendi"}