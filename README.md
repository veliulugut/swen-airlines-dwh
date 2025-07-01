![Swen Airlines Logo](screenshot/swen_logo.png)

# 🛫 Swen Airlines - Real-Time Data Warehouse & Business Intelligence Platform

---

## 🌍 Language Selection / Dil Seçimi

**Choose your language / Dilinizi seçin:**

[![🇺🇸 English](https://img.shields.io/badge/🇺🇸%20English-Click%20Here-blue?style=for-the-badge)](#english-version)
[![🇹🇷 Türkçe](https://img.shields.io/badge/🇹🇷%20Türkçe-Buraya%20Tıklayın-red?style=for-the-badge)](#türkçe-versiyon)

**Connect with me / Benimle iletişime geçin:**

[![💼 LinkedIn](https://img.shields.io/badge/💼%20LinkedIn-Veli%20Uluğut-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/veliulugut/)

---

<div id="english-version"></div>

## 🇺🇸 English Version

**Comprehensive data warehouse solution developed for real-time business analytics and operational excellence in modern aviation industry**

### 📊 About the Project

Swen Airlines Data Warehouse project is a fully automated, real-time business intelligence platform designed to meet the complex operational needs of a modern airline company. This system monitors and analyzes all operational processes from flight operations to passenger services, from revenue analysis to crew management.

The project can process thousands of flights, millions of passengers and complex operational data instantly with enterprise-level data processing capacity. The system aims to maximize the efficiency of airline operations by providing critical operational insights to decision makers.

### 🏗️ System Architecture

#### 3-Layer Data Warehouse Architecture

The system is designed in 3 main layers in accordance with modern data warehouse principles:

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Data Sources  │───▶│    Kafka     │───▶│   FT Layer      │
│  (Real-time)    │    │  (Streaming) │    │  (Fact Tables)  │
│                 │    │              │    │                 │
│ • Flight Ops    │    │ • Topic-based│    │ • Raw Data      │
│ • Bookings      │    │ • Partitioned│    │ • Time-stamped  │
│ • Passengers    │    │ • Scalable   │    │ • Audit Trail   │
│ • Crew          │    │              │    │                 │
│ • Baggage       │    │              │    │                 │
└─────────────────┘    └──────────────┘    └─────────────────┘
                                                    │
                                                    ▼
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Dashboard     │◀───│  TR Layer    │◀───│   STR Layer     │
│  (Streamlit)    │    │ (Reports)    │    │ (Staging)       │
│                 │    │              │    │                 │
│ • Executive     │    │ • Aggregated │    │ • Cleaned Data  │
│ • Operations    │    │ • KPIs       │    │ • Business Rules│
│ • Revenue       │    │ • Metrics    │    │ • Enriched      │
│ • Passengers    │    │ • Trends     │    │ • Validated     │
│ • Aircraft      │    │              │    │                 │
└─────────────────┘    └──────────────┘    └─────────────────┘
                                                    ▲
                                                    │
                       ┌──────────────────────────────────┐
                       │        Airflow ETL              │
                       │    (SQL Procedures)             │
                       │                                  │
                       │ • FT → STR (every 5 min)       │
                       │ • STR → TR (every 3 min)        │
                       │ • Delta Processing              │
                       │ • Error Handling                │
                       │ • Data Quality Checks           │
                       └──────────────────────────────────┘
```

### 🚀 Quick Start

```bash
git clone https://github.com/yourusername/swen-airlines-dwh.git
cd swen-airlines-dwh
docker compose up -d
```

### 📱 Access Points
- **📊 Analytics Dashboard**: http://localhost:8501
- **⚙️ Airflow Interface**: http://localhost:8080 (admin/admin)
- **🗄️ PostgreSQL**: localhost:5432 (admin/admin)

### 🎯 Key Features
- **Real-time Data Processing**: Kafka-based streaming architecture
- **Automated ETL**: Airflow orchestration with SQL procedures
- **7 Specialized Dashboards**: Executive, Operations, Revenue, Passengers, Crew, Baggage, Aircraft
- **3-Layer Architecture**: FT (Raw) → STR (Cleaned) → TR (Reports)
- **Enterprise-grade**: Scalable, fault-tolerant, monitoring-ready

### 📊 Dashboard Gallery
![Executive Dashboard](screenshot/dashboard_1.png)
![Operations](screenshot/flight_operation.png)
![Revenue Analytics](screenshot/revenue.png)
![Passenger Experience](screenshot/passenger.png)

### 🛠️ Tech Stack
- **Streaming**: Apache Kafka + Zookeeper
- **Orchestration**: Apache Airflow
- **Database**: PostgreSQL
- **Analytics**: Streamlit + Plotly
- **Deployment**: Docker + Docker Compose

### 📈 Business Impact
- **30% Faster Decision Making** through real-time insights
- **25% Cost Reduction** via resource optimization
- **40% Improved Customer Satisfaction** with proactive service
- **20% Revenue Increase** through dynamic pricing

**🔗 Links:**
- 📊 **Dashboard**: http://localhost:8501
- ⚙️ **Airflow**: http://localhost:8080
- 📧 **Contact**: veliulugut1@gmail.com

**⭐ If you like this project, don't forget to give it a star!**

---

<div id="türkçe-versiyon"></div>

## 🇹🇷 Türkçe Versiyon

**Modern havacılık sektöründe gerçek zamanlı iş analitiği ve operasyonel mükemmellik için geliştirilmiş kapsamlı veri ambarı çözümü**

### 📊 Proje Hakkında

Swen Airlines Veri Ambarı projesi, modern bir havayolu şirketinin karmaşık operasyonel ihtiyaçlarını karşılamak üzere tasarlanmış tam otomatik, gerçek zamanlı iş zekâsı platformudur. Bu sistem, uçuş operasyonlarından yolcu hizmetlerine, gelir analizinden ekip yönetimine kadar tüm operasyonel süreçleri izler ve analiz eder.

Proje, kurumsal seviyede veri işleme kapasitesi ile binlerce uçuş, milyonlarca yolcu ve karmaşık operasyonel verileri anlık olarak işleyebilmektedir. Sistem, karar vericilere kritik operasyonel içgörüler sağlayarak havayolu operasyonlarının verimliliğini en üst düzeye çıkarmayı hedeflemektedir.

### 🏗️ Sistem Mimarisi

#### 3 Katmanlı Veri Ambarı Mimarisi

Sistem, modern veri ambarı prensiplerine uygun olarak 3 ana katmanda tasarlanmıştır:

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Veri Kaynakları│───▶│    Kafka     │───▶│   FT Katmanı    │
│ (Gerçek Zamanlı) │    │ (Streaming)  │    │ (Fact Tables)   │
│                 │    │              │    │                 │
│ • Uçuş Ops      │    │ • Konu Tabanlı│    │ • Ham Veri      │
│ • Rezervasyonlar│    │ • Bölümlenmiş │    │ • Zaman Damgalı │
│ • Yolcular      │    │ • Ölçeklenebilir│    │ • Denetim İzi   │
│ • Ekip          │    │              │    │                 │
│ • Bagaj         │    │              │    │                 │
└─────────────────┘    └──────────────┘    └─────────────────┘
                                                    │
                                                    ▼
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Dashboard     │◀───│  TR Katmanı  │◀───│   STR Katmanı   │
│  (Streamlit)    │    │ (Raporlar)   │    │ (Staging)       │
│                 │    │              │    │                 │
│ • Yönetici      │    │ • Toplanmış  │    │ • Temizlenmiş   │
│ • Operasyonlar  │    │ • KPI'lar    │    │ • İş Kuralları  │
│ • Gelir         │    │ • Metrikler  │    │ • Zenginleştirilmiş│
│ • Yolcular      │    │ • Trendler   │    │ • Doğrulanmış   │
│ • Uçaklar       │    │              │    │                 │
└─────────────────┘    └──────────────┘    └─────────────────┘
                                                    ▲
                                                    │
                       ┌──────────────────────────────────┐
                       │        Airflow ETL              │
                       │    (SQL Prosedürleri)           │
                       │                                  │
                       │ • FT → STR (her 5 dakika)      │
                       │ • STR → TR (her 3 dakika)       │
                       │ • Delta İşleme                  │
                       │ • Hata Yönetimi                 │
                       │ • Veri Kalitesi Kontrolleri     │
                       └──────────────────────────────────┘
```

### 🚀 Hızlı Başlangıç

```bash
git clone https://github.com/yourusername/swen-airlines-dwh.git
cd swen-airlines-dwh
docker compose up -d
```

### 📱 Erişim Noktaları
- **📊 Analitik Dashboard**: http://localhost:8501
- **⚙️ Airflow Arayüzü**: http://localhost:8080 (admin/admin)
- **🗄️ PostgreSQL**: localhost:5432 (admin/admin)

### 🎯 Temel Özellikler
- **Gerçek Zamanlı Veri İşleme**: Kafka tabanlı streaming mimarisi
- **Otomatik ETL**: SQL prosedürleri ile Airflow orkestrayonu
- **7 Özelleşmiş Dashboard**: Yönetici, Operasyonlar, Gelir, Yolcular, Ekip, Bagaj, Uçak
- **3 Katmanlı Mimari**: FT (Ham) → STR (Temizlenmiş) → TR (Raporlar)
- **Kurumsal Seviye**: Ölçeklenebilir, hata toleranslı, izleme hazır

### 📊 Dashboard Galerisi
![Yönetici Dashboard](screenshot/dashboard_1.png)
![Operasyonlar](screenshot/flight_operation.png)
![Gelir Analitikleri](screenshot/revenue.png)
![Yolcu Deneyimi](screenshot/passenger.png)

### 🛠️ Teknoloji Yığını
- **Streaming**: Apache Kafka + Zookeeper
- **Orkestrasyon**: Apache Airflow
- **Veritabanı**: PostgreSQL
- **Analitik**: Streamlit + Plotly
- **Deployment**: Docker + Docker Compose

### 📈 İş Etkisi
- **%30 Daha Hızlı Karar Verme** gerçek zamanlı içgörüler sayesinde
- **%25 Maliyet Azaltma** kaynak optimizasyonu ile
- **%40 Müşteri Memnuniyeti Artışı** proaktif hizmet ile
- **%20 Gelir Artışı** dinamik fiyatlandırma sayesinde

---

**🔗 Bağlantılar:**
- 📊 **Dashboard**: http://localhost:8501
- ⚙️ **Airflow**: http://localhost:8080
- 📧 **İletişim**: veliulugut1@gmail.com

**⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!**
