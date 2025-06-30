# 🛫 Swen Airlines Data Warehouse (DWH) - Otomatik Sistem

**Gerçek Zamanlı Veri Ambarı ve Analitik Dashboard Sistemi**

## 🚀 **Sistemin Otomatik Çalışma Şekli**

### 📊 **Sistem Mimarisi**

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐    ┌──────────────┐
│   Data Producer │───▶│    Kafka     │───▶│  FT Tables      │───▶│ STR Tables   │
│  (Real-time)    │    │  (Streaming) │    │  (PostgreSQL)   │    │ (Cleaned)    │
└─────────────────┘    └──────────────┘    └─────────────────┘    └──────────────┘
                                                     │                       │
                                                     ▼                       ▼
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐    ┌──────────────┐
│   Dashboard     │◀───│   TR Tables  │◀───│   SQL Procedures │◀───│   Airflow    │
│  (Streamlit)    │    │  (Reports)   │    │   (Transform)    │    │ (Scheduler)  │
└─────────────────┘    └──────────────┘    └─────────────────┘    └──────────────┘
```

## 🔄 **Otomatik Çalışan Süreçler**

### 1️⃣ **Real-Time Data Generation (7/24 Çalışır)**
- **Producer**: `data_gen/producer.py`
- **Görev**: Her 5 dakikada 10 farklı tabloya gerçek zamanlı veri üretir
- **Kafka Topics**: flight, passenger, booking, baggage, crew_assignment, vb.
- **Durum**: Sürekli çalışır (`restart: unless-stopped`)

### 2️⃣ **Real-Time Data Ingestion (Her 5 Dakika)**
- **Consumer**: `consumers/consumer.py` 
- **Airflow DAG**: `ft_kafka_to_postgres_dag.py`
- **Görev**: Kafka'dan veri alıp PostgreSQL FT tablolarına yazar
- **Schedule**: Her 5 dakika
- **Durum**: Airflow scheduler tarafından otomatik tetiklenir

### 3️⃣ **Data Transformation (Her 3 Dakika)**
- **SQL Procedures**: `sql/ddl/10_job_flight.sql` ... `18_job_passenger_notification.sql`
- **Airflow DAG**: `procedures_dag.py`
- **Görev**: FT → STR → TR transformasyonu (9 farklı prosedür)
- **Schedule**: Her 3 dakika
- **Durum**: Delta mode (sadece yeni veriler işlenir)

### 4️⃣ **Real-Time Dashboard (7/24 Erişilebilir)**
- **Frontend**: `dashboard/app.py` (Streamlit)
- **Görev**: TR tablolarından canlı raporlar sunar
- **Sayfalar**: Executive, Operations, Revenue, Passengers, Crew, Baggage, Aircraft
- **Port**: http://localhost:8501

## 🗄️ **Veritabanı Katmanları**

| Katman | Açıklama | Örnekler | Güncelleme |
|--------|----------|----------|------------|
| **FT (Fact)** | Ham gerçek zamanlı veri | ft_flight, ft_passenger, ft_booking | Her 5 dakika (Kafka) |
| **STR (Staging)** | Temizlenmiş, zenginleştirilmiş | str_flight, str_passenger | Her 3 dakika (Prosedür) |
| **TR (Reporting)** | Raporlama ve metrik tabloları | tr_daily_flight_metrics, tr_revenue_summary | Her 3 dakika (Prosedür) |

## 🐳 **Docker Servisleri**

### Core Services
```yaml
postgres:          # PostgreSQL DB (swen_dwh + airflow_db)
zookeeper:         # Kafka koordinasyonu
kafka:             # Message broker
kafka-producer:    # Gerçek zamanlı veri üretimi
```

### Automation Services  
```yaml
data-init:           # İlk veri yükleme (bir kez çalışır)
airflow-webserver:   # Airflow UI (http://localhost:8080)
airflow-scheduler:   # DAG scheduling ve execution
streamlit-dashboard: # Analytics dashboard (http://localhost:8501)
```

## ⚡ **Sistemin Başlatılması**

### Tek Komutla Başlat:
```bash
docker compose up -d
```

### Otomatik Olarak Gerçekleşen İşlemler:
1. **PostgreSQL**: 2 veritabanı (swen_dwh, airflow_db) oluşturur
2. **Kafka**: Topics ve message broker başlatır  
3. **Data Init**: Sample data yükler ve initial prosedürleri çalıştırır
4. **Airflow**: DAG'ları aktif eder ve scheduling başlatır
5. **Producer**: Kafka'ya gerçek zamanlı veri üretmeye başlar
6. **Consumer**: Her 5 dakika Kafka'dan veri çeker
7. **Procedures**: Her 3 dakika data transformation yapar
8. **Dashboard**: Canlı analitik raporları sunar

## 📊 **Dashboard Özellikleri**

### 7 Ana Sayfa:
- **Executive Dashboard**: KPI'lar, genel metrikler
- **Operations**: Uçuş durumları, gecikme analizi
- **Revenue**: Gelir analizi, satış performansı  
- **Passengers**: Yolcu segmentasyonu, sadakat analizi
- **Crew**: Ekip utilization, shift analizi
- **Baggage**: Bagaj istatistikleri, kayıp/hasar analizi
- **Aircraft**: Uçak performansı, yakıt/bakım analizi

### Modern UI Features:
- **Dark Theme**: Modern görünüm
- **Real-time Updates**: Canlı veri 
- **Interactive Charts**: Plotly tabanlı grafikler
- **KPI Cards**: Önemli metrikler
- **Responsive Design**: Mobile uyumlu

## 🔧 **Monitoring ve Yönetim**

### Airflow UI (http://localhost:8080)
- **Username**: admin
- **Password**: admin
- **DAG Monitoring**: Real-time execution tracking
- **Error Handling**: Failed task notifications

### Database Access
```bash
# PostgreSQL'e bağlan
docker exec -it swen-airlines-dwh-postgres-1 psql -U admin -d swen_dwh

# Tablo durumları kontrol et
SELECT schemaname, tablename, n_tup_ins, n_tup_upd 
FROM pg_stat_user_tables 
WHERE tablename LIKE 'tr_%';
```

### System Status Check
```bash
# Sistemin genel durumunu kontrol et
python scripts/system_status.py
```

### Log Monitoring
```bash
# Tüm servislerin logları
docker compose logs -f

# Specific service logs
docker logs swen-airlines-dwh-kafka-producer-1 -f
docker logs swen-airlines-dwh-airflow-scheduler-1 -f
```

## 📁 **Proje Yapısı**

```
swen-airlines-dwh/
├── 📊 dashboard/           # Streamlit Dashboard
│   └── app.py             # 7 sayfalık analitik dashboard
├── 🔄 dags/               # Airflow DAGs
│   ├── ft_kafka_to_postgres_dag.py  # Kafka → PostgreSQL (5 dk)
│   └── procedures_dag.py             # Data transformation (3 dk)
├── 📡 data_gen/           # Real-time Data Generation  
│   ├── producer.py        # Kafka producer (7/24 çalışır)
│   ├── generators.py      # Fake data generators
│   └── config.py          # Kafka konfigürasyonu
├── 🍺 consumers/          # Kafka Data Ingestion
│   └── consumer.py        # Kafka → PostgreSQL consumer
├── 🗂️ sql/ddl/           # Database Schema & Procedures
│   ├── 01_create_ft_tables.sql      # FT tables schema
│   ├── 10_job_flight.sql ... 18_*   # 9 transformation procedures
│   └── 03_fn_truncate_table.sql     # Utility functions
├── ⚙️ scripts/            # Automation Scripts
│   ├── setup_airflow_connections.py # Airflow connections
│   ├── load_sample_data.py          # Initial data loading
│   ├── run_initial_procedures.py    # First-time procedures
│   └── activate_dags.py             # DAG activation
└── 🐳 docker-compose.yml  # Complete system orchestration
```

## 🎯 **Sistem Avantajları**

✅ **Fully Automated**: Sıfır manuel müdahale
✅ **Real-time**: 3-5 dakika veri freshness
✅ **Scalable**: Yeni tablolar/prosedürler kolayca eklenebilir  
✅ **Fault Tolerant**: Airflow retry mechanisms
✅ **Modern UI**: Professional BI dashboard
✅ **Monitoring**: Comprehensive logging ve alerting
✅ **Docker**: Tek komutla deployment

## 🔧 **Özelleştirme**

### Yeni Veri Kaynağı Ekleme:
1. `data_gen/generators.py`: Yeni fake data generator
2. `data_gen/producer.py`: Yeni Kafka topic 
3. `consumers/consumer.py`: Yeni topic mapping
4. `sql/ddl/`: Yeni tablo ve prosedür
5. `dashboard/app.py`: Yeni dashboard sayfası

### Schedule Değiştirme:
- Kafka ingestion: `dags/ft_kafka_to_postgres_dag.py` → `schedule_interval`
- Data transformation: `dags/procedures_dag.py` → `schedule_interval`

---
**🚀 Tek Komutla Başlat:** `docker compose up -d`  
**📊 Dashboard:** http://localhost:8501  
**⚙️ Airflow:** http://localhost:8080
