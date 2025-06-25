import json
import threading
from kafka import KafkaConsumer
from sqlalchemy import create_engine, Table, MetaData, insert
from sqlalchemy.exc import SQLAlchemyError
from data_gen.config import (
    KAFKA_BROKER,
    KAFKA_TOPIC_FLIGHT, KAFKA_TOPIC_PASSENGER, KAFKA_TOPIC_BOOKING, KAFKA_TOPIC_BAGGAGE,
    KAFKA_TOPIC_CREW_ASSIGNMENT, KAFKA_TOPIC_PASSENGER_NOTIFICATION, KAFKA_TOPIC_FLIGHT_INCIDENT,
    KAFKA_TOPIC_PASSENGER_FEEDBACK, KAFKA_TOPIC_FLIGHT_FUEL, KAFKA_TOPIC_MAINTENANCE_EVENT
)

# PostgreSQL bağlantı ayarları (gerekirse config.py'ye taşı)
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
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=f'{topic}_consumer_group'
    )

def insert_batch(table, records):
    if not records:
        return
    with engine.begin() as conn:
        try:
            conn.execute(insert(table), records)
            print(f"[Consumer] {len(records)} kayıt {table.name} tablosuna yüklendi.")
        except SQLAlchemyError as e:
            print(f"[Consumer][ERROR] DB insert error: {e}")

def consume_topic(topic: str, table):
    consumer = get_consumer(topic)
    batch = []
    for msg in consumer:
        batch.append(msg.value)
        if len(batch) >= 100:  # Batch size
            insert_batch(table, batch)
            batch.clear()

if __name__ == "__main__":
    print("[Consumer] Kafka consumer başlatıldı. Tüm FT tabloları dinleniyor.")
    tables = {name: Table(name, metadata, autoload_with=engine) for name in topic_table_map.values()}
    threads = []
    for topic, table_name in topic_table_map.items():
        t = threading.Thread(target=consume_topic, args=(topic, tables[table_name]), daemon=True)
        t.start()
        threads.append(t)
    for t in threads:
        t.join() 