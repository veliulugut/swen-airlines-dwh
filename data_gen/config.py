# Database Configuration
POSTGRES_URI = 'postgresql+psycopg2://admin:admin@postgres/swen_dwh'

# Kafka Configuration - Confluent Platform
KAFKA_BROKER = 'kafka:29092'  # Internal listener için
KAFKA_TOPIC_FLIGHT = 'ft_flight'
KAFKA_TOPIC_PASSENGER = 'ft_passenger'
KAFKA_TOPIC_BOOKING = 'ft_booking'
KAFKA_TOPIC_BAGGAGE = 'ft_baggage'
KAFKA_TOPIC_CREW_ASSIGNMENT = 'ft_crew_assignment'
KAFKA_TOPIC_PASSENGER_NOTIFICATION = 'ft_passenger_notification'
KAFKA_TOPIC_FLIGHT_INCIDENT = 'ft_flight_incident'
KAFKA_TOPIC_PASSENGER_FEEDBACK = 'ft_passenger_feedback'
KAFKA_TOPIC_FLIGHT_FUEL = 'ft_flight_fuel'
KAFKA_TOPIC_MAINTENANCE_EVENT = 'ft_maintenance_event'

BATCH_SIZE_FLIGHT = 50
BATCH_SIZE_PASSENGER = 100
BATCH_SIZE_BOOKING = 80
BATCH_SIZE_BAGGAGE = 80
BATCH_SIZE_CREW_ASSIGNMENT = 30
BATCH_SIZE_PASSENGER_NOTIFICATION = 50
BATCH_SIZE_FLIGHT_INCIDENT = 10
BATCH_SIZE_PASSENGER_FEEDBACK = 30
BATCH_SIZE_FLIGHT_FUEL = 20
BATCH_SIZE_MAINTENANCE_EVENT = 10

PRODUCE_INTERVAL_SECONDS = 60  # 1 dakika - Airflow her 5 dakikada bir toplasın 