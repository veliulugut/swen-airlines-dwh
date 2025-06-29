import json
import time
from kafka import KafkaConsumer
from sqlalchemy import create_engine, Table, MetaData, insert
from sqlalchemy.exc import SQLAlchemyError
from data_gen.config import (
    KAFKA_BROKER,
    KAFKA_TOPIC_FLIGHT, KAFKA_TOPIC_PASSENGER, KAFKA_TOPIC_BOOKING, KAFKA_TOPIC_BAGGAGE,
    KAFKA_TOPIC_CREW_ASSIGNMENT, KAFKA_TOPIC_PASSENGER_NOTIFICATION, KAFKA_TOPIC_FLIGHT_INCIDENT,
    KAFKA_TOPIC_PASSENGER_FEEDBACK, KAFKA_TOPIC_FLIGHT_FUEL, KAFKA_TOPIC_MAINTENANCE_EVENT
)

# PostgreSQL bağlantı ayarları
POSTGRES_URI = 'postgresql+psycopg2://admin:admin@postgres/swen_dwh'

# SQLAlchemy engine ve metadata
engine = create_engine(POSTGRES_URI)
metadata = MetaData()

topic_table_map = {
    KAFKA_TOPIC_FLIGHT: 'ft_flight',
    KAFKA_TOPIC_PASSENGER: 'ft_passenger',
    KAFKA_TOPIC_BOOKING: 'ft_booking',
    KAFKA_TOPIC_BAGGAGE: 'ft_baggage',
    KAFKA_TOPIC_CREW_ASSIGNMENT: 'ft_crew_assignment',
    KAFKA_TOPIC_PASSENGER_NOTIFICATION: 'ft_passenger_notification',
    KAFKA_TOPIC_FLIGHT_INCIDENT: 'ft_flight_incident',
    KAFKA_TOPIC_PASSENGER_FEEDBACK: 'ft_passenger_feedback',
    KAFKA_TOPIC_FLIGHT_FUEL: 'ft_flight_fuel',
    KAFKA_TOPIC_MAINTENANCE_EVENT: 'ft_maintenance_event',
}

def get_consumer(topic: str) -> KafkaConsumer:
    return KafkaConsumer(
        topic,
        bootstrap_servers=[KAFKA_BROKER],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='latest',  # Son 5 dakikalık veriyi almak için latest kullan
        enable_auto_commit=True,
        group_id=f'{topic}_airflow_consumer_group',
        consumer_timeout_ms=30000  # 30 saniye timeout
    )

def insert_batch(table, records):
    if not records:
        return 0
    with engine.begin() as conn:
        try:
            conn.execute(insert(table), records)
            print(f"[Consumer] {len(records)} kayıt {table.name} tablosuna yüklendi.")
            return len(records)
        except SQLAlchemyError as e:
            print(f"[Consumer][ERROR] DB insert error: {e}")
            return 0

def consume_topic_batch(topic: str, table, timeout_seconds=300):
    """Belirli bir topic'ten timeout süresi boyunca veri tüketir"""
    consumer = get_consumer(topic)
    batch = []
    start_time = time.time()
    
    print(f"[Consumer] {topic} topic'inden veri tüketimi başladı...")
    
    try:
        for msg in consumer:
            batch.append(msg.value)
            
            # Timeout kontrolü
            if time.time() - start_time > timeout_seconds:
                break
                
            # Batch size kontrolü
            if len(batch) >= 100:
                inserted = insert_batch(table, batch)
                print(f"[Consumer] {topic}: {inserted} kayıt işlendi")
                batch.clear()
        
        # Kalan verileri işle
        if batch:
            inserted = insert_batch(table, batch)
            print(f"[Consumer] {topic}: Son {inserted} kayıt işlendi")
            
    except Exception as e:
        print(f"[Consumer][ERROR] {topic} tüketim hatası: {e}")
    finally:
        consumer.close()
    
    print(f"[Consumer] {topic} tüketimi tamamlandı.")

def run_kafka_to_postgres_batch():
    """Airflow task olarak çağrılacak ana fonksiyon"""
    print("[Consumer] Kafka'dan PostgreSQL'e batch transfer başlatıldı")
    
    # Tabloları yükle
    try:
        tables = {name: Table(name, metadata, autoload_with=engine) for name in topic_table_map.values()}
        print(f"[Consumer] {len(tables)} tablo yüklendi")
    except Exception as e:
        print(f"[Consumer][ERROR] Tablo yükleme hatası: {e}")
        return
    
    total_processed = 0
    
    # Her topic için batch processing
    for topic, table_name in topic_table_map.items():
        try:
            print(f"[Consumer] {topic} işleniyor...")
            consume_topic_batch(topic, tables[table_name], timeout_seconds=60)
        except Exception as e:
            print(f"[Consumer][ERROR] {topic} işleme hatası: {e}")
    
    print(f"[Consumer] Kafka'dan PostgreSQL'e batch transfer tamamlandı")

if __name__ == "__main__":
    run_kafka_to_postgres_batch() 