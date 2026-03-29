import pymysql
import pymysql.cursors
from datetime import datetime
import json

def get_connection():
    return pymysql.connect(
        host     = "localhost",
        user     = "root",
        password = "Ankara10.",
        database = "mugla_disaster",
        cursorclass = pymysql.cursors.DictCursor  
    )

def save_to_db(data):
    conn = get_connection()
    cursor = conn.cursor()

    for p in data:
        cursor.execute("""
            INSERT INTO weather_data 
                (name, lat, lon, poi_type, vegetation, temperature, humidity, wind, light,
                 elevation, slope_deg, slope_risk, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                temperature = VALUES(temperature),
                humidity    = VALUES(humidity),
                wind        = VALUES(wind),
                light       = VALUES(light),
                vegetation  = VALUES(vegetation),
                elevation   = VALUES(elevation),
                slope_deg   = VALUES(slope_deg),
                slope_risk  = VALUES(slope_risk),
                updated_at  = VALUES(updated_at)
        """, (
            p["name"], p["lat"], p["lon"], p["poi_type"], p["vegetation"],
            p["temperature"], p["humidity"], p["wind"], p["light"],
            p.get("elevation", 0), p.get("slope_deg", 0), p.get("slope_risk", 0),
            datetime.now()
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"{len(data)} kayıt veritabanına yazıldı")

    

def load_from_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather_data ORDER BY updated_at DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def is_data_fresh():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(updated_at) as last_update FROM weather_data")
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result is None:
        return False

    last_updated = result.get("last_update")

    if last_updated is None:
        return False

    fark = (datetime.now() - last_updated).total_seconds() / 60
    print(f"Son güncelleme: {fark:.0f} dakika önce")
    return fark < 10

def save_roads_to_db(roads):
    conn = get_connection()
    cursor = conn.cursor()
    for r in roads:
        cursor.execute("""
            INSERT INTO road_data (id, road_type, safety, geometry, updated_at)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                road_type  = VALUES(road_type),
                safety     = VALUES(safety),
                geometry   = VALUES(geometry),
                updated_at = VALUES(updated_at)
        """, (
            r["id"], r["type"], r["safety"],
            json.dumps(r["geometry"]),
            datetime.now()
        ))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"{len(roads)} yol kaydedildi")

def load_roads_from_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM road_data")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    for r in rows:
        r["geometry"] = json.loads(r["geometry"])
    return rows