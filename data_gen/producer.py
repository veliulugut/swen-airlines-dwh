import json
import time
from kafka import KafkaProducer
from data_gen.generators import (
    generate_ft_flight, generate_ft_passenger, generate_ft_booking, generate_ft_baggage,
    generate_ft_crew_assignment, generate_ft_passenger_notification, generate_ft_flight_incident,
    generate_ft_passenger_feedback, generate_ft_flight_fuel, generate_ft_maintenance_event
)
from data_gen.config import (
    KAFKA_BROKER,
    KAFKA_TOPIC_FLIGHT, KAFKA_TOPIC_PASSENGER, KAFKA_TOPIC_BOOKING, KAFKA_TOPIC_BAGGAGE,
    KAFKA_TOPIC_CREW_ASSIGNMENT, KAFKA_TOPIC_PASSENGER_NOTIFICATION, KAFKA_TOPIC_FLIGHT_INCIDENT,
    KAFKA_TOPIC_PASSENGER_FEEDBACK, KAFKA_TOPIC_FLIGHT_FUEL, KAFKA_TOPIC_MAINTENANCE_EVENT,
    BATCH_SIZE_FLIGHT, BATCH_SIZE_PASSENGER, BATCH_SIZE_BOOKING, BATCH_SIZE_BAGGAGE,
    BATCH_SIZE_CREW_ASSIGNMENT, BATCH_SIZE_PASSENGER_NOTIFICATION, BATCH_SIZE_FLIGHT_INCIDENT,
    BATCH_SIZE_PASSENGER_FEEDBACK, BATCH_SIZE_FLIGHT_FUEL, BATCH_SIZE_MAINTENANCE_EVENT,
    PRODUCE_INTERVAL_SECONDS
)

def get_kafka_producer() -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER],
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        linger_ms=10
    )

def produce_batch(producer: KafkaProducer):
    # Önce ana ID'leri üret
    flights = generate_ft_flight(BATCH_SIZE_FLIGHT)
    passengers = generate_ft_passenger(BATCH_SIZE_PASSENGER)
    flight_ids = [f["flight_id"] for f in flights]
    passenger_ids = [p["passenger_id"] for p in passengers]

    # Diğer FT tabloları için ilişkili veri üret
    bookings = generate_ft_booking(BATCH_SIZE_BOOKING, passenger_ids, flight_ids)
    booking_ids = [b["booking_id"] for b in bookings]
    baggages = generate_ft_baggage(BATCH_SIZE_BAGGAGE, booking_ids)
    crew_assignments = generate_ft_crew_assignment(BATCH_SIZE_CREW_ASSIGNMENT, flight_ids)
    notifications = generate_ft_passenger_notification(BATCH_SIZE_PASSENGER_NOTIFICATION, passenger_ids, flight_ids)
    incidents = generate_ft_flight_incident(BATCH_SIZE_FLIGHT_INCIDENT, flight_ids)
    feedbacks = generate_ft_passenger_feedback(BATCH_SIZE_PASSENGER_FEEDBACK, passenger_ids, flight_ids)
    fuels = generate_ft_flight_fuel(BATCH_SIZE_FLIGHT_FUEL, flight_ids)
    maintenance_events = generate_ft_maintenance_event(BATCH_SIZE_MAINTENANCE_EVENT)

    # Kafka'ya publish et
    for obj, topic in [
        (flights, KAFKA_TOPIC_FLIGHT),
        (passengers, KAFKA_TOPIC_PASSENGER),
        (bookings, KAFKA_TOPIC_BOOKING),
        (baggages, KAFKA_TOPIC_BAGGAGE),
        (crew_assignments, KAFKA_TOPIC_CREW_ASSIGNMENT),
        (notifications, KAFKA_TOPIC_PASSENGER_NOTIFICATION),
        (incidents, KAFKA_TOPIC_FLIGHT_INCIDENT),
        (feedbacks, KAFKA_TOPIC_PASSENGER_FEEDBACK),
        (fuels, KAFKA_TOPIC_FLIGHT_FUEL),
        (maintenance_events, KAFKA_TOPIC_MAINTENANCE_EVENT)
    ]:
        for record in obj:
            producer.send(topic, record)
    producer.flush()
    print(f"[Producer] Batch gönderildi: {len(flights)} flight, {len(passengers)} passenger, {len(bookings)} booking, {len(baggages)} baggage, {len(crew_assignments)} crew_assignment, {len(notifications)} notification, {len(incidents)} incident, {len(feedbacks)} feedback, {len(fuels)} fuel, {len(maintenance_events)} maintenance_event.")

def main():
    producer = get_kafka_producer()
    print("[Producer] Kafka producer başlatıldı. Her 5 dakikada bir tüm FT tabloları için veri üretilecek.")
    while True:
        produce_batch(producer)
        time.sleep(PRODUCE_INTERVAL_SECONDS)

if __name__ == "__main__":
    main() 