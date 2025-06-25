# 🧩 Ürün Gereksinimleri Dokümanı (PRD) – Swen Airlines DWH

**Proje Adı:** Swen Airlines Veri Ambarı (DWH)
**Yazar:** Data Engineering Lead
**Tarih:** 2025-06-23
**Versiyon:** v2.0 – Gerçek Zamanlı Analitik için Geliştirildi
**Durum:** Geliştirme Aşamasında

---

## 🎯 Proje Amacı

Swen Airlines için geliştirilecek olan DWH çözümünün temel amacı:

- Uçuş, yolcu, rezervasyon, gelir ve operasyonel süreçleri analiz edebilmek
- Gerçek zamanlı dashboardlarla karar destek sistemlerini güçlendirmek
- Realtime veri akışı ile analiz gecikmelerini ortadan kaldırmak
- KPI ve metriklerle operasyonel verimliliği artırmak

---

## 🏗️ Hedef Mimari

### Katmanlar:

1. **FT (Fact Tables)** – Gerçek zamanlı olay katmanı
2. **STR (Staging & Transformation)** – Temizlenmiş, zenginleştirilmiş ara katman
3. **TR (Transactional Reporting)** – Raporlama ve özet tablolar
4. **DM (Dimension Models)** – Lookup & yavaş değişen boyutlar
5. **BI Layer** – Apache Superset / Power BI

### Veri Akışı:

Kafka (Ops DB CDC) → Python ETL (Faker/Airflow) → FT Tables (PostgreSQL)
→ Stored Procedures → STR Tables
→ Aggregated Views → TR Layer
→ Materialized Views + Superset/Power BI Dashboard

### Teknolojiler:

- PostgreSQL 16
- Python 3.11 (Faker, SQLAlchemy, psycopg2)
- Apache Airflow (ETL orkestrasyonu)
- Apache Superset (BI)
- Docker Compose
- pg_cron / Debezium (Gerçek zamanlı veri)

---

## 🧱 DWH Veri Modeli (Tablolar ve Alanlar)

### 1️⃣ Fact Tabloları (FT)

#### FT_FLIGHT
**Amaç:** Uçuşlara ait tüm operasyonel ve zaman bazlı detayların tutulduğu ana tablodur.
- flight_id (UUID, PK): Uçuşun benzersiz anahtarı
- flight_number (VARCHAR, SWXXXX): Uçuş numarası
- departure_airport (VARCHAR, ICAO): Kalkış havalimanı kodu
- arrival_airport (VARCHAR, ICAO): Varış havalimanı kodu
- scheduled_departure (TIMESTAMP): Planlanan kalkış zamanı
- actual_departure (TIMESTAMP): Gerçekleşen kalkış zamanı
- aircraft_id (UUID, FK): Uçağın referans anahtarı
- flight_status (VARCHAR): Uçuş durumu (Scheduled, Delayed, Cancelled)
- weather_condition (VARCHAR): Kalkış anındaki hava durumu
- cancellation_reason (VARCHAR): Varsa iptal nedeni
- delay_reason (VARCHAR): Varsa gecikme nedeni
- origin_country (VARCHAR): Kalkış ülke kodu
- destination_country (VARCHAR): Varış ülke kodu
- distance_km (FLOAT): Uçuş mesafesi (km)
- flight_duration_min (INT): Uçuş süresi (dakika)
- is_international (BOOLEAN): Uluslararası mı?
- gate_number (VARCHAR): Kalkış kapı numarası

#### FT_PASSENGER
**Amaç:** Yolculara ait kimlik, iletişim ve sadakat bilgilerini tutar.
- passenger_id (UUID, PK): Yolcunun benzersiz anahtarı
- full_name (VARCHAR): Ad soyad
- birth_date (DATE): Doğum tarihi
- nationality (VARCHAR, ISO 3166): Uyruk
- frequent_flyer (BOOLEAN): Sadakat programı üyesi mi?
- loyalty_tier (VARCHAR): Sadakat seviyesi (Bronze, Silver, Gold, Platinum)
- email (VARCHAR): E-posta
- phone_number (VARCHAR): Telefon numarası
- gender (VARCHAR): Cinsiyet
- registration_date (DATE): Sisteme kayıt tarihi
- passport_number (VARCHAR): Pasaport numarası

#### FT_BOOKING
**Amaç:** Rezervasyon işlemlerinin ve bilet satışlarının detaylarını tutar.
- booking_id (UUID, PK): Rezervasyon anahtarı
- passenger_id (UUID, FK): Yolcu referansı
- flight_id (UUID, FK): Uçuş referansı
- booking_date (TIMESTAMP): Rezervasyon tarihi
- cancel_date (TIMESTAMP): Varsa iptal tarihi
- is_cancelled (BOOLEAN): İptal durumu
- fare_class (VARCHAR): Bilet sınıfı (Economy, Business, First)
- ticket_price (DECIMAL): Satış fiyatı
- seat_number (VARCHAR): Koltuk numarası
- booking_channel (VARCHAR): Satış kanalı (Website, Mobile, Agent)
- payment_method (VARCHAR): Ödeme yöntemi (Credit Card, Miles, Voucher)
- currency (VARCHAR): Para birimi
- discount_applied (BOOLEAN): İndirim uygulandı mı?
- promo_code (VARCHAR): Kullanılan promosyon kodu

#### FT_BAGGAGE
**Amaç:** Yolcu bagajlarının detaylarını ve durumunu izler.
- baggage_id (UUID, PK): Bagaj anahtarı
- booking_id (UUID, FK): Rezervasyon referansı
- baggage_type (VARCHAR): Bagaj tipi (Checked, Carry-on)
- weight_kg (FLOAT): Bagaj ağırlığı
- is_special_handling (BOOLEAN): Özel taşıma gereksinimi var mı?
- baggage_status (VARCHAR): Bagaj durumu (Loaded, Lost, Damaged, Delivered)

#### FT_CREW_ASSIGNMENT
**Amaç:** Uçuşlara atanan ekip üyelerinin görev ve zaman detaylarını tutar.
- assignment_id (UUID, PK): Atama anahtarı
- flight_id (UUID, FK): Uçuş referansı
- crew_id (UUID, FK): Ekip üyesi referansı
- role (VARCHAR): Görev (Pilot, Attendant, Engineer)
- shift_start (TIMESTAMP): Görev başlangıcı
- shift_end (TIMESTAMP): Görev bitişi
- is_lead (BOOLEAN): Baş görevli mi?
- assignment_status (VARCHAR): Atama durumu (Confirmed, Pending, Cancelled)

#### FT_PASSENGER_NOTIFICATION
**Amaç:** Yolculara gönderilen bildirimlerin ve iletim durumlarının kaydı.
- notification_id (UUID, PK): Bildirim anahtarı
- passenger_id (UUID, FK): Yolcu referansı
- flight_id (UUID, FK, opsiyonel): Uçuş referansı
- notification_type (VARCHAR): Bildirim türü (Delay, Cancel, Promo, vb.)
- message_content (TEXT): Mesaj içeriği
- send_time (TIMESTAMP): Gönderim zamanı
- delivery_channel (VARCHAR): Kanal (SMS, EMAIL, PUSH)
- delivery_status (VARCHAR): Durum (Sent, Failed, Pending)
- read_status (BOOLEAN): Okundu mu?

#### FT_FLIGHT_INCIDENT
**Amaç:** Uçuş sırasında yaşanan olay ve aksaklıkların kaydı.
- incident_id (UUID, PK): Olay anahtarı
- flight_id (UUID, FK): Uçuş referansı
- incident_type (VARCHAR): Olay türü (Medical, Technical, Security)
- description (TEXT): Açıklama
- reported_time (TIMESTAMP): Bildirim zamanı
- resolved_time (TIMESTAMP): Çözüm zamanı
- severity (VARCHAR): Ciddiyet (Low, Medium, High)

#### FT_PASSENGER_FEEDBACK
**Amaç:** Yolcu geri bildirimleri ve memnuniyet skorlarının kaydı.
- feedback_id (UUID, PK): Geri bildirim anahtarı
- passenger_id (UUID, FK): Yolcu referansı
- flight_id (UUID, FK): Uçuş referansı
- feedback_type (VARCHAR): Tür (Complaint, Praise, Suggestion)
- feedback_text (TEXT): Geri bildirim metni
- rating (INT, 1-5): Puan
- submitted_at (TIMESTAMP): Gönderim zamanı

#### FT_FLIGHT_FUEL (Yeni)
**Amaç:** Uçuşlara yapılan yakıt ikmali ve yakıt tüketimi detaylarını tutar.
- fuel_id (UUID, PK): Yakıt kaydı anahtarı
- flight_id (UUID, FK): Uçuş referansı
- fuel_type (VARCHAR): Yakıt tipi
- fuel_quantity_liters (FLOAT): Yakıt miktarı (litre)
- fueling_time (TIMESTAMP): Yakıt ikmal zamanı
- fueling_company (VARCHAR): Yakıt tedarikçi şirketi

#### FT_MAINTENANCE_EVENT (Yeni)
**Amaç:** Uçaklara yapılan bakım işlemlerinin ve maliyetlerinin kaydı.
- maintenance_id (UUID, PK): Bakım kaydı anahtarı
- aircraft_id (UUID, FK): Uçak referansı
- event_type (VARCHAR): Bakım türü (Scheduled, Unscheduled)
- description (TEXT): Açıklama
- event_time (TIMESTAMP): Bakım başlangıcı
- resolved_time (TIMESTAMP): Bakım bitişi
- cost (DECIMAL): Bakım maliyeti

### 2️⃣ Dimension Tabloları (DM)

#### DM_AIRCRAFT
**Amaç:** Uçaklara ait teknik ve kimlik bilgilerinin tutulduğu referans tablosu.
- aircraft_id (UUID, PK): Uçak anahtarı
- model (VARCHAR): Uçak modeli
- capacity (INT): Yolcu kapasitesi
- manufacturer (VARCHAR): Üretici firma
- engine_type (VARCHAR): Motor tipi
- registration_number (VARCHAR): Kayıt numarası

#### DM_AIRPORT
**Amaç:** Havalimanı kimlik ve konum bilgilerinin tutulduğu referans tablosu.
- airport_code (VARCHAR, PK): Havalimanı kodu
- name (VARCHAR): Havalimanı adı
- city (VARCHAR): Şehir
- country (VARCHAR): Ülke
- timezone (VARCHAR): Zaman dilimi
- latitude (FLOAT): Enlem
- longitude (FLOAT): Boylam

#### DM_CREW
**Amaç:** Ekip üyelerinin kimlik, lisans ve görev bilgilerinin tutulduğu referans tablosu.
- crew_id (UUID, PK): Ekip anahtarı
- full_name (VARCHAR): Ad soyad
- role (VARCHAR): Görev
- hire_date (DATE): İşe başlama tarihi
- license_number (VARCHAR): Lisans numarası
- nationality (VARCHAR): Uyruk
- gender (VARCHAR): Cinsiyet
- home_base_airport (VARCHAR): Ana üs havalimanı
- contact_number (VARCHAR): İletişim numarası

#### DM_WEATHER
**Amaç:** Hava durumu kodları ve meteorolojik detayların tutulduğu referans tablosu.
- weather_code (VARCHAR, PK): Hava durumu kodu
- description (VARCHAR): Açıklama
- impact_level (VARCHAR): Etki seviyesi (Low, Medium, High)
- temperature_c (FLOAT): Sıcaklık (°C)
- wind_speed_kph (FLOAT): Rüzgar hızı (km/s)
- visibility_km (FLOAT): Görüş mesafesi (km)
- precipitation_mm (FLOAT): Yağış miktarı (mm)

#### DM_FLIGHT_ROUTE (Yeni)
**Amaç:** Uçuş rotalarının ve mesafe/süre bilgilerinin tutulduğu referans tablosu.
- route_id (UUID, PK): Rota anahtarı
- departure_airport (VARCHAR, FK): Kalkış havalimanı
- arrival_airport (VARCHAR, FK): Varış havalimanı
- route_code (VARCHAR): Rota kodu
- distance_km (FLOAT): Rota mesafesi (km)
- typical_duration_min (INT): Tipik uçuş süresi (dk)

#### DM_MAINTENANCE_COMPANY (Yeni)
**Amaç:** Bakım hizmeti veren şirketlerin kimlik ve iletişim bilgilerinin tutulduğu referans tablosu.
- company_id (UUID, PK): Şirket anahtarı
- company_name (VARCHAR): Şirket adı
- contact_number (VARCHAR): İletişim numarası
- country (VARCHAR): Ülke

---

## 🖥️ BI Dashboard Tasarımları ve Raporlama

### 1. Operasyonel Dashboard
**Tablolar:** FT_FLIGHT, DM_AIRPORT, DM_WEATHER, FT_FLIGHT_INCIDENT, DM_FLIGHT_ROUTE
- Uçuş durumu (Pie/Bar Chart)
- Havalimanı bazında kalkış/varış yoğunluğu (Heatmap)
- Gecikme ve iptal nedenleri (Bar Chart)
- Hava durumu etkisi (Scatter/Correlation Chart)
- Anlık uçuş listesi (Tablo)
- Uçuş rotası performansı (Line/Bar Chart)
- Olay/incident analizi (Tablo)

### 2. Gelir ve Satış Dashboardu
**Tablolar:** FT_BOOKING, TR_REVENUE_SUMMARY, DM_AIRPORT, FT_PASSENGER_FEEDBACK
- Günlük/aylık toplam gelir (Line Chart)
- Sınıf bazında gelir dağılımı (Stacked Bar)
- Satış kanalı performansı (Pie Chart)
- İptal ve iade oranları (KPI Card)
- En çok kullanılan promosyonlar (Tablo)
- Yolcu memnuniyeti ve geri bildirim analizi (Bar/Histogram)

### 3. Yolcu Analitiği Dashboardu
**Tablolar:** FT_PASSENGER, FT_PASSENGER_NOTIFICATION, FT_PASSENGER_FEEDBACK, TR_PASSENGER_SEGMENTATION
- Sadakat programı dağılımı (Donut Chart)
- Segment bazlı yolcu sayısı (Bar Chart)
- Bildirim opt-in oranı (KPI)
- Yolcu memnuniyeti (Rating Histogram)
- Bildirim performansı (Tablo)
- Yolcu segmentasyonu ve davranış analizi (Cluster/Scatter)

### 4. Ekip ve Kaynak Kullanımı Dashboardu
**Tablolar:** FT_CREW_ASSIGNMENT, DM_CREW, TR_CREW_UTILIZATION, FT_MAINTENANCE_EVENT
- Ekip bazında uçuş ve shift dağılımı (Gantt/Bar Chart)
- Ortalama shift süresi (KPI)
- Domestic vs International görev oranı (Pie Chart)
- Ekip performans sıralaması (Tablo)
- Bakım etkinliği ve maliyet analizi (Line/Bar Chart)

### 5. Bagaj ve Operasyonel İzleme
**Tablolar:** FT_BAGGAGE, FT_FLIGHT, DM_AIRPORT
- Bagaj tipi ve ağırlık dağılımı (Histogram)
- Özel taşıma gereksinimi olan bagajlar (KPI)
- Bagaj kayıp/hasar oranları (Line Chart)

### 6. Yakıt ve Bakım Dashboardu (Yeni)
**Tablolar:** FT_FLIGHT_FUEL, FT_MAINTENANCE_EVENT, DM_MAINTENANCE_COMPANY, DM_AIRCRAFT
- Uçuş bazında yakıt tüketimi (Line Chart)
- Yakıt tipi ve tedarikçi analizi (Pie/Bar Chart)
- Bakım türü ve maliyet dağılımı (Bar Chart)
- Bakım şirketi performansı (Tablo)

### 7. KPI & Uyarı Paneli
**Tablolar:** TR_DAILY_FLIGHT_METRICS, FT_FLIGHT_INCIDENT, FT_BOOKING
- SLA dışı gecikmeler (KPI)
- Anomali tespiti (Alert Table)
- Otomatik uyarı ve bildirimler (Tablo)

---

## 📅 Yol Haritası

| Hafta | Hedef                                          |
| ----- | ---------------------------------------------- |
| 1     | Altyapı kurulumu, PostgreSQL setup             |
| 2     | FT_FLIGHT + FT_PASSENGER üretimi               |
| 3     | Booking, Baggage, Crew assignment verisi       |
| 4     | STR prosedürler, TR katmanı                    |
| 5     | Realtime reporting + Monitoring kurulumu       |
| 6     | BI dashboard entegrasyon, final kalite kontrol |

---

## 📂 Dosya Yapısı

```
.
├── dags/
├── docker-compose.yml
├── dockerfile
├── logs/
├── plugins/
├── sql/
│   └── ddl/
│       └── 01_create_ft_tables.sql
└── README.md
```

---

## 💡 Genişletilebilirlik

- IoT uçak sensör verisi entegrasyonu
- Hava durumu tahmini ve ML modelleri
- Yeni FT/DM tabloları eklenebilir

---

## 🔄 Katmanlar Arası Veri Akışı ve BI Besleme Mantığı

### Katmanlar ve Akış

- **FT (Fact Table):** Kaynak transactional veri (ham veri, CDC/ETL ile gelir)
- **STR (Staging):** FT'den alınan, temizlenmiş ve zenginleştirilmiş staging tabloları (AS SELECT ... ile oluşturulur)
- **TR (Transactional Reporting):** STR'den beslenen, raporlama için optimize edilmiş, prosedürlerle incremental güncellenen final rapor tabloları
- **BI:** Genellikle TR (rapor) tabloları kullanılır, bazı özel durumlarda STR/FT'den de veri çekilebilir
- **DM (Dimension):** Lookup/enrich için her katmanda kullanılır

### BI Dashboardları ve Beslendiği Katmanlar

| Dashboard/Paneller                | Ana Kaynak Tablo (BI)         | Beslendiği Katman | Akış (Kaynak → BI)                                                                 | Açıklama/Bağlantı                                                                 |
|-----------------------------------|-------------------------------|-------------------|------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| Operasyonel Dashboard             | TR_DAILY_FLIGHT_METRICS       | TR                | FT_FLIGHT → STR_FLIGHT → TR_DAILY_FLIGHT_METRICS                                   | Uçuş, gecikme, iptal, hava durumu, DM_AIRPORT, DM_WEATHER ile enrich edilir       |
| Gelir & Satış Dashboardu          | TR_REVENUE_SUMMARY            | TR                | FT_BOOKING → STR_BOOKING → TR_REVENUE_SUMMARY                                      | Sınıf, kanal, promosyon, DM_AIRPORT enrich                                        |
| Yolcu Analitiği Dashboardu        | TR_PASSENGER_SEGMENTATION     | TR                | FT_PASSENGER, FT_BOOKING, FT_PASSENGER_FEEDBACK → STR_* → TR_PASSENGER_SEGMENTATION| Sadakat, segment, bildirim, feedback, DM_PASSENGER enrich                         |
| Ekip & Kaynak Kullanımı Dashboardu| TR_CREW_UTILIZATION           | TR                | FT_CREW_ASSIGNMENT → STR_CREW_ASSIGNMENT → TR_CREW_UTILIZATION                     | DM_CREW enrich, shift, görev, uçuş türü                                           |
| Bagaj Dashboardu                  | TR_BAGGAGE_METRICS (opsiyonel)| TR                | FT_BAGGAGE → STR_BAGGAGE → TR_BAGGAGE_METRICS                                      | Bagaj tipi, ağırlık, DM_AIRPORT enrich                                            |
| Yakıt & Bakım Dashboardu          | TR_FUEL_CONSUMPTION, TR_MAINTENANCE_SUMMARY | TR | FT_FLIGHT_FUEL, FT_MAINTENANCE_EVENT → STR_* → TR_*                                | DM_AIRCRAFT, DM_MAINTENANCE_COMPANY enrich                                        |
| KPI & Uyarı Paneli                | TR_DAILY_FLIGHT_METRICS, TR_FLIGHT_INCIDENT_SUMMARY | TR | FT_FLIGHT, FT_FLIGHT_INCIDENT → STR_* → TR_*                                       | SLA, anomaly, alert, DM_AIRPORT enrich                                            |

### Katmanlar Arası Bağlantı ve Yükleme Mantığı

- **FT → STR:**  STR tabloları, FT'den `AS SELECT` ile oluşturulur. Temizlik, tarih normalizasyonu, lookup (join) ve kalite flag'leri burada yapılır.
- **STR → TR:**  TR tabloları, STR'den prosedürlerle (genellikle `INSERT ... SELECT ... WHERE insert_date > last_load_date`) incremental/delta olarak güncellenir. TR tabloları genellikle materialized view veya fiziksel tablo olur.
- **TR → BI:**  BI araçları (Power BI, Superset) doğrudan TR tablolarına bağlanır. Bazı özel durumlarda STR veya FT'den de veri çekilebilir, ancak önerilen yol TR'dir.

### Örnek: Operasyonel Dashboard Akışı

1. **FT_FLIGHT:** Ham uçuş verisi (CDC/ETL ile gelir)
2. **STR_FLIGHT:**  FT_FLIGHT'ten alınır, hatalı kayıtlar temizlenir, DM_AIRPORT ve DM_WEATHER ile enrich edilir, insert_date, update_date eklenir
3. **TR_DAILY_FLIGHT_METRICS:**  STR_FLIGHT'ten günlük bazda uçuş, gecikme, iptal, ortalama gecikme, hava durumu etkisi gibi metrikler hesaplanır, prosedür ile incremental yüklenir
4. **BI:**  TR_DAILY_FLIGHT_METRICS tablosu dashboardda kullanılır

### Katmanlar Arası Bağlantı Diyagramı (Metinsel)

```
FT_* (ham veri)
   │
   ▼
STR_* (temizlenmiş, enrich edilmiş veri)
   │
   ▼
TR_* (rapor/metrik tablosu)
   │
   ▼
BI Dashboard (Power BI / Superset)
```

- **DM_* tabloları** her aşamada lookup/enrich için kullanılır.

### Kısa Notlar

- Tüm prosedürler incremental (delta) çalışacak şekilde insert_date veya update_date referans alınarak yazılır.
- BI raporları TR katmanından beslenir, böylece performans ve veri tutarlılığı sağlanır.
- FT ve STR tabloları, veri izlenebilirliği ve hata ayıklama için de kullanılabilir.
