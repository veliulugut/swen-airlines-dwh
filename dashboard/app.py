import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import sys
import os

# Path ayarlama
sys.path.append('/app')
from data_gen.config import POSTGRES_URI

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="Swen Airlines DWH Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database bağlantısı
@st.cache_resource
def get_database_connection():
    try:
        engine = create_engine(POSTGRES_URI)
        return engine
    except Exception as e:
        st.error(f"Veritabanı bağlantı hatası: {e}")
        return None

# Veri çekme fonksiyonu
@st.cache_data(ttl=30)  # 30 saniye cache
def fetch_data(query):
    engine = get_database_connection()
    if engine:
        try:
            return pd.read_sql(query, engine)
        except Exception as e:
            st.error(f"Veri çekme hatası: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

# Tablo bilgileri
TABLES = {
    'ft_flight': {
        'name': 'Uçuş Verileri',
        'icon': '✈️',
        'description': 'Uçuş operasyonları ve durum bilgileri'
    },
    'ft_passenger': {
        'name': 'Yolcu Verileri',
        'icon': '👤',
        'description': 'Yolcu profil ve demografik bilgiler'
    },
    'ft_booking': {
        'name': 'Rezervasyon Verileri',
        'icon': '📝',
        'description': 'Rezervasyon ve bilet satış verileri'
    },
    'ft_baggage': {
        'name': 'Bagaj Verileri',
        'icon': '🧳',
        'description': 'Bagaj takip ve işleme verileri'
    },
    'ft_crew_assignment': {
        'name': 'Mürettebat Atamaları',
        'icon': '👨‍✈️',
        'description': 'Mürettebat görev atamaları'
    },
    'ft_passenger_notification': {
        'name': 'Yolcu Bildirimleri',
        'icon': '📱',
        'description': 'Yolcu bildirim ve iletişim verileri'
    },
    'ft_flight_incident': {
        'name': 'Uçuş Olayları',
        'icon': '⚠️',
        'description': 'Uçuş süresince yaşanan olaylar'
    },
    'ft_passenger_feedback': {
        'name': 'Yolcu Geri Bildirimleri',
        'icon': '⭐',
        'description': 'Yolcu memnuniyet ve geri bildirimler'
    },
    'ft_flight_fuel': {
        'name': 'Yakıt Verileri',
        'icon': '⛽',
        'description': 'Uçak yakıt tüketim verileri'
    },
    'ft_maintenance_event': {
        'name': 'Bakım Olayları',
        'icon': '🔧',
        'description': 'Uçak bakım ve onarım kayıtları'
    }
}

def main():
    st.title("🛫 Swen Airlines Data Warehouse Dashboard")
    st.markdown("---")

    # Sidebar menü
    st.sidebar.title("📊 Dashboard Menüsü")
    page = st.sidebar.selectbox(
        "Sayfa Seçin:",
        ["Ana Sayfa"] + [f"{info['icon']} {info['name']}" for info in TABLES.values()]
    )

    if page == "Ana Sayfa":
        show_overview()
    else:
        # Seçilen tabloyu bul
        for table_name, table_info in TABLES.items():
            if page == f"{table_info['icon']} {table_info['name']}":
                show_table_details(table_name, table_info)
                break

def show_overview():
    st.header("📈 Genel Bakış")
    
    # Tablo istatistikleri
    col1, col2, col3, col4 = st.columns(4)
    
    total_records = 0
    tables_with_data = 0
    
    for i, (table_name, table_info) in enumerate(TABLES.items()):
        count_query = f"SELECT COUNT(*) as count FROM {table_name}"
        count_df = fetch_data(count_query)
        
        if not count_df.empty:
            count = count_df.iloc[0]['count']
            total_records += count
            if count > 0:
                tables_with_data += 1
        else:
            count = 0
            
        # Metrik kartları
        if i % 4 == 0:
            with col1:
                st.metric(
                    label=f"{table_info['icon']} {table_info['name']}",
                    value=f"{count:,}"
                )
        elif i % 4 == 1:
            with col2:
                st.metric(
                    label=f"{table_info['icon']} {table_info['name']}",
                    value=f"{count:,}"
                )
        elif i % 4 == 2:
            with col3:
                st.metric(
                    label=f"{table_info['icon']} {table_info['name']}",
                    value=f"{count:,}"
                )
        else:
            with col4:
                st.metric(
                    label=f"{table_info['icon']} {table_info['name']}",
                    value=f"{count:,}"
                )
    
    st.markdown("---")
    
    # Özet istatistikler
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🗃️ Toplam Kayıt", f"{total_records:,}")
    
    with col2:
        st.metric("📊 Aktif Tablo", f"{tables_with_data}")
    
    with col3:
        st.metric("🕐 Son Güncelleme", datetime.now().strftime("%H:%M:%S"))
    
    st.markdown("---")
    
    # Son 24 saat veri akışı grafiği
    st.subheader("📊 Son 24 Saat Veri Akışı")
    
    # Her tablo için son 24 saat veri girişleri
    data_flow = []
    for table_name in TABLES.keys():
        query = f"""
        SELECT DATE_TRUNC('hour', ingestion_time) as hour,
               COUNT(*) as count
        FROM {table_name}
        WHERE ingestion_time >= NOW() - INTERVAL '24 hours'
        GROUP BY hour
        ORDER BY hour
        """
        df = fetch_data(query)
        if not df.empty:
            df['table'] = TABLES[table_name]['name']
            data_flow.append(df)
    
    if data_flow:
        combined_df = pd.concat(data_flow, ignore_index=True)
        fig = px.line(combined_df, x='hour', y='count', color='table',
                     title='Saatlik Veri Girişi',
                     labels={'hour': 'Saat', 'count': 'Kayıt Sayısı'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Henüz son 24 saat içinde veri bulunamadı.")

def show_table_details(table_name, table_info):
    st.header(f"{table_info['icon']} {table_info['name']}")
    st.write(table_info['description'])
    st.markdown("---")
    
    # Tablo istatistikleri
    col1, col2, col3, col4 = st.columns(4)
    
    # Toplam kayıt sayısı
    count_query = f"SELECT COUNT(*) as count FROM {table_name}"
    count_df = fetch_data(count_query)
    total_count = count_df.iloc[0]['count'] if not count_df.empty else 0
    
    with col1:
        st.metric("📊 Toplam Kayıt", f"{total_count:,}")
    
    # Son 24 saat
    recent_query = f"""
    SELECT COUNT(*) as count 
    FROM {table_name} 
    WHERE ingestion_time >= NOW() - INTERVAL '24 hours'
    """
    recent_df = fetch_data(recent_query)
    recent_count = recent_df.iloc[0]['count'] if not recent_df.empty else 0
    
    with col2:
        st.metric("🕐 Son 24 Saat", f"{recent_count:,}")
    
    # İşlenen kayıtlar
    processed_query = f"SELECT COUNT(*) as count FROM {table_name} WHERE is_processed = true"
    processed_df = fetch_data(processed_query)
    processed_count = processed_df.iloc[0]['count'] if not processed_df.empty else 0
    
    with col3:
        st.metric("✅ İşlenmiş", f"{processed_count:,}")
    
    # Son veri girişi
    last_query = f"SELECT MAX(ingestion_time) as last_time FROM {table_name}"
    last_df = fetch_data(last_query)
    last_time = last_df.iloc[0]['last_time'] if not last_df.empty and last_df.iloc[0]['last_time'] else "Henüz veri yok"
    
    with col4:
        if isinstance(last_time, str):
            st.metric("🕒 Son Veri", last_time)
        else:
            st.metric("🕒 Son Veri", last_time.strftime("%H:%M:%S"))
    
    st.markdown("---")
    
    # Son veriler tablosu
    st.subheader("📋 Son Veriler")
    
    # İlk 100 kaydı göster
    sample_query = f"""
    SELECT * FROM {table_name} 
    ORDER BY ingestion_time DESC 
    LIMIT 100
    """
    sample_df = fetch_data(sample_query)
    
    if not sample_df.empty:
        st.dataframe(sample_df, use_container_width=True)
        
        # CSV indirme
        csv = sample_df.to_csv(index=False)
        st.download_button(
            label="📥 CSV İndir",
            data=csv,
            file_name=f"{table_name}_data.csv",
            mime="text/csv"
        )
    else:
        st.info("Bu tabloda henüz veri bulunmuyor.")
    
    # Zaman bazlı analiz
    if not sample_df.empty and 'ingestion_time' in sample_df.columns:
        st.subheader("📈 Zaman Bazlı Analiz")
        
        time_query = f"""
        SELECT DATE_TRUNC('hour', ingestion_time) as hour,
               COUNT(*) as count
        FROM {table_name}
        WHERE ingestion_time >= NOW() - INTERVAL '7 days'
        GROUP BY hour
        ORDER BY hour
        """
        time_df = fetch_data(time_query)
        
        if not time_df.empty:
            fig = px.bar(time_df, x='hour', y='count',
                        title='Son 7 Gün Saatlik Veri Girişi',
                        labels={'hour': 'Saat', 'count': 'Kayıt Sayısı'})
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main() 