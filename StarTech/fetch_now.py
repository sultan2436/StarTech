from data import get_dataset, get_roads

data = get_dataset()
print(f"{len(data)} nokta çekildi")
for d in data:
    print(f"{d['name']} → {d['temperature']}°C | {d['wind']} km/h | {d['humidity']}% | {d['vegetation']} | eğim: {d.get('slope_deg', 'YOK')}° | yükseklik: {d.get('elevation', 'YOK')}m")



print("\n Yol verisi çekiliyor...")
roads = get_roads()
print(f"{len(roads)} yol çekildi")