 EERIS+ — Afet Karar Destek Sistemi
## Orman Yangını Risk Analizi ve Yayılım Tahmin Sistemi

EERIS+, orman yangınlarını sadece tespit etmekle kalmayıp, yangının nasıl yayılacağını önceden tahmin eden ve müdahale süreçlerini optimize eden bir karar destek sistemidir.

> “Yangını takip eden değil, yöneten sistem.”

---

## 🚀 Proje Amacı

Türkiye’de orman yangınlarının en büyük problemi, yangının çıkması değil, **nasıl yayılacağının bilinmemesidir**.

Bu proje:
- Yangın riskini önceden hesaplar  
- Yangının yayılım yönünü tahmin eder  
- Etkilenecek bölgeleri belirler  
- Müdahale ve tahliye süreçlerini optimize eder  

---

## 🧠 Sistem Nasıl Çalışır?

Sistem ardışık bir karar zinciri olarak çalışır:

Veri → Risk → Yayılım → Etki (POI) → Rota → Karar

1. Uydu ve meteorolojik veriler alınır  
2. Risk analizi yapılır  
3. Yangın yayılımı tahmin edilir  
4. Etkilenecek bölgeler (POI) belirlenir  
5. En güvenli rota oluşturulur  

---

## 📊 Özellikler

### 🔥 Risk Analizi
- Rüzgar, nem, sıcaklık, bitki örtüsü ve eğim verileri kullanılır  
- 0–1 arası risk skoru hesaplanır  

### 🌪 Yayılım Tahmini
- Rüzgar yönü ve hızına göre yangının yönü belirlenir  
- Gelecekteki risk tahmin edilir  

### 🏠 Etki Analizi (POI)
- Hastane, okul, köy ve kritik bölgeler analiz edilir  
- Önceliklendirme yapılır  

### 🚒 Rota Optimizasyonu
- En kısa değil, en güvenli rota hesaplanır  
- Riskli bölgelerden kaçınılır  

---

## 🧩 Kullanılan Teknolojiler

- **Backend:** FastAPI  
- **Frontend:** Leaflet.js  
- **Veritabanı:** MySQL  
- **Dil:** Python  

---

## 🌍 Veri Kaynakları

- Uydu verileri (yangın tespiti)  
- Meteorolojik veriler (rüzgar, nem, sıcaklık)  
- OpenStreetMap (yol ve POI verileri)  
- Open-Meteo (eğim ve yükseklik verileri)  

---

## 📈 Model Yaklaşımı

Sistem hibrit bir model kullanır:

- **Kural tabanlı model (fizik)**
- **Makine öğrenmesi (Random Forest)**

  final_spread = base_model * 0.7 + ml_model * 0.3

  Bu sayede:
- Fiziksel doğruluk korunur  
- Veri ile optimize edilir  

---

## 🗺 Sistem Çıktıları

- Risk haritası  
- Yangın yayılım simülasyonu  
- Kritik bölge analizi  
- Tahliye öncelik listesi  
- Güvenli rota önerisi  

---

## 🎯 Hedef Kullanıcılar

- AFAD  
- Orman Genel Müdürlüğü  
- Belediyeler  
- İtfaiye ekipleri  

---

## ⚡ Neden EERIS+?

- Reaktif değil, **proaktif sistem**  
- Sadece veri değil, **karar üretir**  
- Yangını değil, **davranışını model eder**  

---

## 🔮 Gelecek Geliştirmeler

- Gerçek zamanlı uydu entegrasyonu  
- IoT sensör desteği  
- Farklı afet türlerine uyarlama (sel, deprem)  
- Mobil bildirim sistemi  

---

## 👥 Ekip

- **Sultan Top** — Veri Bilimi & Risk Modelleme  
- **Esma Genç** — Backend & Veri Mühendisliği  
- **Sudenur Çakır** — Frontend & Görselleştirme  

---

## 📌 Sonuç

EERIS+, yangınları sadece tespit eden bir sistem değil,  
**yangının geleceğini tahmin ederek doğru müdahaleyi yöneten bir karar motorudur.**
