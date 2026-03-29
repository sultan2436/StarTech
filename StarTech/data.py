import requests
from datetime import datetime
from database import save_to_db, load_from_db, is_data_fresh
from database import save_roads_to_db, load_roads_from_db
import math
import time
import threading
_data_lock = threading.Lock()
_data_cache = None

API_KEY = "9f87fe7461a186ff53ea6ee6806e40f3"

MUGLA_POIS = [
    # === HASTANELER ===
    {"name": "Muğla Eğitim Araştırma Hastanesi", "lat": 37.2153, "lon": 28.3636, "poi_type": "hospital", "vegetation": "urban"},
    {"name": "Marmaris Devlet Hastanesi",         "lat": 36.8555, "lon": 28.2771, "poi_type": "hospital", "vegetation": "urban"},
    {"name": "Bodrum Devlet Hastanesi",            "lat": 37.0344, "lon": 27.4305, "poi_type": "hospital", "vegetation": "urban"},
    {"name": "Fethiye Devlet Hastanesi",           "lat": 36.6556, "lon": 29.1243, "poi_type": "hospital", "vegetation": "urban"},
    {"name": "Köyceğiz Devlet Hastanesi",          "lat": 36.9728, "lon": 28.6833, "poi_type": "hospital", "vegetation": "urban"},

    # === OKULLAR ===
    {"name": "Milas İlçe Merkezi",   "lat": 37.3167, "lon": 27.7833, "poi_type": "school", "vegetation": "urban"},
    {"name": "Datça İlçe Merkezi",   "lat": 36.7269, "lon": 27.6908, "poi_type": "school", "vegetation": "maki"},
    {"name": "Ortaca İlçe Merkezi",  "lat": 36.8333, "lon": 28.7667, "poi_type": "school", "vegetation": "urban"},
    {"name": "Yatağan İlçe Merkezi", "lat": 37.3333, "lon": 28.1333, "poi_type": "school", "vegetation": "urban"},
    {"name": "Seydikemer Merkezi",   "lat": 36.7500, "lon": 29.0000, "poi_type": "school", "vegetation": "urban"},

    # === ORMAN KÖYLERİ ===
    {"name": "Turunç Köyü",      "lat": 36.7700, "lon": 28.2800, "poi_type": "village", "vegetation": "kizilcam"},
    {"name": "Bayır Köyü",       "lat": 36.9200, "lon": 28.3500, "poi_type": "village", "vegetation": "kizilcam"},
    {"name": "Hisarönü",         "lat": 36.8100, "lon": 28.1600, "poi_type": "village", "vegetation": "maki"},
    {"name": "Orhaniye Köyü",    "lat": 36.9000, "lon": 28.2200, "poi_type": "village", "vegetation": "kizilcam"},
    {"name": "Selimiye Köyü",    "lat": 36.8300, "lon": 28.1900, "poi_type": "village", "vegetation": "kizilcam"},
    {"name": "Çamlı Köyü",      "lat": 36.8700, "lon": 28.1700, "poi_type": "village", "vegetation": "kizilcam"},
    {"name": "Çetibeli Köyü",    "lat": 36.9300, "lon": 28.2100, "poi_type": "village", "vegetation": "kizilcam"},
    {"name": "Karaca Köyü",      "lat": 36.9500, "lon": 28.1500, "poi_type": "village", "vegetation": "maki"},
    {"name": "Karacasöğüt Köyü", "lat": 36.9500, "lon": 28.1000, "poi_type": "village", "vegetation": "maki"},
    {"name": "Gökova Köyü",      "lat": 37.0300, "lon": 28.3500, "poi_type": "village", "vegetation": "kizilcam"},
    {"name": "Kıran Köyü",       "lat": 37.0500, "lon": 28.3200, "poi_type": "village", "vegetation": "mesek"},
    {"name": "Kuyucak Köyü",     "lat": 37.0700, "lon": 28.3000, "poi_type": "village", "vegetation": "mesek"},
    {"name": "Sarnıç Köyü",      "lat": 37.0200, "lon": 28.4000, "poi_type": "village", "vegetation": "kizilcam"},
    {"name": "Çiçekli Köyü",     "lat": 37.1000, "lon": 28.4500, "poi_type": "village", "vegetation": "kizilcam"},
    {"name": "Armutçuk Köyü",    "lat": 37.1200, "lon": 28.4200, "poi_type": "village", "vegetation": "kizilcam"},
    {"name": "Kıyra Köyü",       "lat": 37.0800, "lon": 28.4700, "poi_type": "village", "vegetation": "kizilcam"},
    {"name": "Emecik Köyü",      "lat": 36.7800, "lon": 27.5800, "poi_type": "village", "vegetation": "maki"},
    {"name": "Kovanlık Köyü",    "lat": 36.7500, "lon": 27.6200, "poi_type": "village", "vegetation": "maki"},
    {"name": "Döğüşbelen Köyü",  "lat": 37.0200, "lon": 28.7000, "poi_type": "village", "vegetation": "zeytin"},
    {"name": "Hamitköy",         "lat": 36.9500, "lon": 28.7200, "poi_type": "village", "vegetation": "mesek"},

    # === AHIRLAR ===
    {"name": "Kavaklıdere Çiftliği", "lat": 37.4333, "lon": 28.3833, "poi_type": "farm", "vegetation": "mesek"},
    {"name": "Menteşe Ahırları",     "lat": 37.1800, "lon": 28.3000, "poi_type": "farm", "vegetation": "urban"},
    {"name": "Çamarası Çiftliği",    "lat": 37.0600, "lon": 27.5500, "poi_type": "farm", "vegetation": "maki"},
    {"name": "Sakar Ormanı Ahır",    "lat": 37.0500, "lon": 28.6000, "poi_type": "farm", "vegetation": "kizilcam"},
    {"name": "Yatağan Büyükbaş",     "lat": 37.3500, "lon": 28.1500, "poi_type": "farm", "vegetation": "urban"},
    {"name": "Milas Küçükbaş",       "lat": 37.2900, "lon": 27.8200, "poi_type": "farm", "vegetation": "zeytin"},
]


def fetch_weather(lat, lon):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    )
    try:
        d = requests.get(url, timeout=5, verify=False).json()
        return {
            "temperature": round(d["main"]["temp"], 2),
            "humidity":    round(d["main"]["humidity"], 2),
            "wind":        round(d["wind"]["speed"] * 3.6, 2),
            "light":       round(1 - d["clouds"]["all"] / 100, 2)
        }
    except Exception as e:
        print(f"API hatası ({lat},{lon}): {e}")
        return {"temperature": 38.0, "humidity": 25.0, "wind": 15.0, "light": 0.7}


def fetch_elevation(coords):
    """[(lat,lon), ...] listesi alır, aynı sırada yükseklik listesi döner"""
    lats = ",".join(str(c[0]) for c in coords)
    lons = ",".join(str(c[1]) for c in coords)
    url = f"https://api.open-meteo.com/v1/elevation?latitude={lats}&longitude={lons}"
    try:
        r = requests.get(url, timeout=10, verify=False)
        return r.json().get("elevation", [])
    except Exception as e:
        print(f"Elevation hatası: {e}")
        return [200] * len(coords)


def calculate_slope(lat, lon):
    """Merkez noktanın 4 yönüne bakarak eğim hesaplar"""
    offset = 0.001  # ~100 metre
    coords = [
        (lat + offset, lon),  # kuzey
        (lat - offset, lon),  # güney
        (lat, lon + offset),  # doğu
        (lat, lon - offset),  # batı
        (lat, lon),           # merkez
    ]
    elevations = fetch_elevation(coords)

    if len(elevations) < 5:
        return {"elevation": 200, "slope_deg": 0, "slope_risk": 0}

    n, s, e, w, c = elevations
    dist = offset * 111000

    slope_ns = abs(n - s) / (2 * dist)
    slope_ew = abs(e - w) / (2 * dist)
    slope_deg = math.degrees(math.atan(math.sqrt(slope_ns**2 + slope_ew**2)))

    return {
        "elevation":  round(c, 1),
        "slope_deg":  round(slope_deg, 2),
        "slope_risk": round(min(slope_deg / 45, 1.0), 3)
    }


def get_dataset():
    global _data_cache
    
    with _data_lock:
        if _data_cache is not None:
            return _data_cache
        
        if is_data_fresh():
            print("Veritabanından yüklendi")
            _data_cache = load_from_db()
            return _data_cache

        print("OpenWeather + Elevation'dan çekiliyor...")
        fresh = []
        for poi in MUGLA_POIS:
            weather    = fetch_weather(poi["lat"], poi["lon"])
            slope_data = calculate_slope(poi["lat"], poi["lon"])
            time.sleep(0.3)
            
            fresh.append({
                "name":        poi["name"],
                "lat":         poi["lat"],
                "lon":         poi["lon"],
                "poi_type":    poi["poi_type"],
                "vegetation":  poi["vegetation"],
                "temperature": weather["temperature"],
                "humidity":    weather["humidity"],
                "wind":        weather["wind"],
                "light":       weather["light"],
                "elevation":   slope_data["elevation"],
                "slope_deg":   slope_data["slope_deg"],
                "slope_risk":  slope_data["slope_risk"],
            })
            print(f"  {poi['name']} → {weather['temperature']}°C | eğim: {slope_data['slope_deg']}°")

        save_to_db(fresh)
        _data_cache = fresh
        return fresh


def get_roads():
    existing = load_roads_from_db()
    if existing:
        print(f"Yollar DB'den yüklendi ({len(existing)} yol)")
        return existing

    print("OSM'den yollar çekiliyor...")
    query = """
    [out:json][timeout:60];
    (
      way["highway"~"primary|secondary|tertiary"]
         (36.7,27.8,37.3,28.9);
    );
    out geom qt;
    """
    try:
        response = requests.post(
            "https://overpass-api.de/api/interpreter",
            data={"data": query},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=60,
            verify=False
        )
        if response.status_code != 200:
            print(f"API hatası: {response.status_code}")
            return []

        roads = []
        for way in response.json().get("elements", []):
            highway_type = way.get("tags", {}).get("highway", "unknown")
            safety = {"primary": 0.9, "secondary": 0.75, "tertiary": 0.6}.get(highway_type, 0.4)
            roads.append({
                "id":       way["id"],
                "type":     highway_type,
                "safety":   safety,
                "geometry": way.get("geometry", [])
            })

        if roads:
            save_roads_to_db(roads)
            print(f"{len(roads)} yol kaydedildi")
        else:
            print("Yol bulunamadı")

        return roads

    except Exception as e:
        print(f"OSM hatası: {e}")
        return []