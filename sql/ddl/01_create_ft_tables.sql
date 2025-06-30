DROP TABLE IF EXISTS FT_FLIGHT_FUEL CASCADE;
DROP TABLE IF EXISTS FT_MAINTENANCE_EVENT CASCADE;
DROP TABLE IF EXISTS FT_PASSENGER_NOTIFICATION CASCADE;
DROP TABLE IF EXISTS FT_FLIGHT_INCIDENT CASCADE;
DROP TABLE IF EXISTS FT_PASSENGER_FEEDBACK CASCADE;
DROP TABLE IF EXISTS FT_BAGGAGE CASCADE;
DROP TABLE IF EXISTS FT_CREW_ASSIGNMENT CASCADE;
DROP TABLE IF EXISTS FT_BOOKING CASCADE;
DROP TABLE IF EXISTS FT_PASSENGER CASCADE;
DROP TABLE IF EXISTS FT_FLIGHT CASCADE;

-- ETL Procedure Log Table (Required for procedures)
CREATE TABLE IF NOT EXISTS etl_procedure_log (
    log_id SERIAL PRIMARY KEY,
    procedure_name VARCHAR(100) NOT NULL,
    step_name VARCHAR(100) NOT NULL,
    source_table VARCHAR(100),
    target_table VARCHAR(100),
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    error_message TEXT,
    row_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS FT_FLIGHT (
    flight_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    flight_number VARCHAR NOT NULL,
    departure_airport VARCHAR NOT NULL,
    arrival_airport VARCHAR NOT NULL,
    scheduled_departure TIMESTAMP NOT NULL,
    actual_departure TIMESTAMP,
    aircraft_id UUID NOT NULL,
    flight_status VARCHAR NOT NULL,
    weather_condition VARCHAR,
    cancellation_reason VARCHAR,
    delay_reason VARCHAR,
    origin_country VARCHAR,
    destination_country VARCHAR,
    distance_km FLOAT,
    flight_duration_min INT,
    is_international BOOLEAN,
    gate_number VARCHAR,
    ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS FT_PASSENGER (
    passenger_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name VARCHAR NOT NULL,
    birth_date DATE,
    nationality VARCHAR,
    frequent_flyer BOOLEAN,
    loyalty_tier VARCHAR,
    email VARCHAR,
    phone_number VARCHAR,
    gender VARCHAR,
    registration_date DATE,
    passport_number VARCHAR,
    ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS FT_BOOKING (
    booking_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    passenger_id UUID NOT NULL,
    flight_id UUID NOT NULL,
    booking_date TIMESTAMP NOT NULL,
    cancel_date TIMESTAMP,
    is_cancelled BOOLEAN,
    fare_class VARCHAR,
    ticket_price DECIMAL,
    seat_number VARCHAR,
    booking_channel VARCHAR,
    payment_method VARCHAR,
    currency VARCHAR,
    discount_applied BOOLEAN,
    promo_code VARCHAR,
    ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS FT_BAGGAGE (
    baggage_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_id UUID NOT NULL,
    baggage_type VARCHAR,
    weight_kg FLOAT,
    is_special_handling BOOLEAN,
    baggage_status VARCHAR,
    ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS FT_CREW_ASSIGNMENT (
    assignment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    flight_id UUID NOT NULL,
    crew_id UUID NOT NULL,
    role VARCHAR,
    shift_start TIMESTAMP,
    shift_end TIMESTAMP,
    is_lead BOOLEAN,
    assignment_status VARCHAR,
    ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS FT_PASSENGER_NOTIFICATION (
    notification_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    passenger_id UUID NOT NULL,
    flight_id UUID,
    notification_type VARCHAR,
    message_content TEXT,
    send_time TIMESTAMP,
    delivery_channel VARCHAR,
    delivery_status VARCHAR,
    read_status BOOLEAN,
    ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS FT_FLIGHT_INCIDENT (
    incident_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    flight_id UUID NOT NULL,
    incident_type VARCHAR,
    description TEXT,
    reported_time TIMESTAMP,
    resolved_time TIMESTAMP,
    severity VARCHAR,
    ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS FT_PASSENGER_FEEDBACK (
    feedback_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    passenger_id UUID NOT NULL,
    flight_id UUID NOT NULL,
    feedback_type VARCHAR,
    feedback_text TEXT,
    rating INT,
    submitted_at TIMESTAMP,
    ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS FT_FLIGHT_FUEL (
    fuel_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    flight_id UUID NOT NULL,
    fuel_type VARCHAR,
    fuel_quantity_liters FLOAT,
    fueling_time TIMESTAMP,
    fueling_company VARCHAR,
    ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS FT_MAINTENANCE_EVENT (
    maintenance_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aircraft_id UUID NOT NULL,
    event_type VARCHAR,
    description TEXT,
    event_time TIMESTAMP,
    resolved_time TIMESTAMP,
    cost DECIMAL,
    ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

create table public.str_baggage as(
SELECT A.*,NOW()::timestamp(0) AS insert_date FROM public.ft_baggage A
WHERE 1=2);

create table public.tr_baggage as(
SELECT A.*,NOW()::timestamp(0) AS insert_date FROM public.ft_baggage A
WHERE 1=2);

create table public.tr_booking as (
    select b.*, now()::timestamp(0) AS insert_date from ft_booking b
                                                   where 1=2
);

create table public.str_booking as (
    select b.*, now()::timestamp(0) AS insert_date from ft_booking b
                                                   where 1=2
);

create table public.str_crew_assignment as(
    SELECT C.*, NOW()::timestamp(0) AS INSERT_DATE FROM PUBLIC.ft_crew_assignment C
    WHERE 1=2
);

create table public.tr_crew_assignment as(
    SELECT C.*, NOW()::timestamp(0) AS INSERT_DATE FROM PUBLIC.ft_crew_assignment C
    WHERE 1=2
);


create table public.str_flight as(
    SELECT F.*, NOW()::timestamp(0) AS INSERT_DATE FROM ft_flight F
    WHERE 1=2
);

create table public.tr_flight as(
    SELECT F.*, NOW()::timestamp(0) AS INSERT_DATE FROM ft_flight F
    WHERE 1=2
);

create table public.str_flight_incident as(
    SELECT F.*, NOW()::timestamp(0) AS INSERT_DATE FROM ft_flight_incident F
    WHERE 1=2
);

create table public.tr_flight_incident as(
    SELECT F.*, NOW()::timestamp(0) AS INSERT_DATE FROM ft_flight_incident F
    WHERE 1=2
);

create table public.str_flight_fuel as(
    SELECT F.*, NOW()::timestamp(0) AS INSERT_DATE FROM ft_flight_fuel F
    WHERE 1=2
);

create table public.tr_flight_fuel as(
    SELECT F.*, NOW()::timestamp(0) AS INSERT_DATE FROM ft_flight_fuel F
    WHERE 1=2
);

create table public.str_maintenance_event as(
    SELECT E.*, NOW()::timestamp(0) AS INSERT_DATE FROM ft_maintenance_event E
    WHERE 1=2
);

create table public.tr_maintenance_event as(
    SELECT E.*, NOW()::timestamp(0) AS INSERT_DATE FROM ft_maintenance_event E
    WHERE 1=2
);

create table public.str_passenger as(
    SELECT P.*, NOW()::timestamp(0) AS INSERT_DATE FROM ft_passenger P
    WHERE 1=2
);

create table public.tr_passenger as(
    SELECT P.*, NOW()::timestamp(0) AS INSERT_DATE FROM ft_passenger P
    WHERE 1=2
);

create table public.str_passenger_feedback as(
    SELECT C.*, NOW()::timestamp(0) AS INSERT_DATE FROM ft_passenger_feedback C
    WHERE 1=2
);

create table public.tr_passenger_feedback as(
    SELECT C.*, NOW()::timestamp(0) AS INSERT_DATE FROM ft_passenger_feedback C
    WHERE 1=2
);

create table public.str_passenger_notification as(
    SELECT A.*, NOW()::timestamp(0) AS INSERT_DATE FROM ft_passenger_notification A
    WHERE 1=2
);

create table public.tr_passenger_notification as(
    SELECT A.*, NOW()::timestamp(0) AS INSERT_DATE FROM ft_passenger_notification A
    WHERE 1=2
);



-- FT_FLIGHT indexes
CREATE INDEX idx_ft_flight_ingestion_time ON FT_FLIGHT(ingestion_time);
CREATE INDEX idx_ft_flight_processed ON FT_FLIGHT(is_processed);
CREATE INDEX idx_ft_flight_number ON FT_FLIGHT(flight_number);
CREATE INDEX idx_ft_flight_departure_date ON FT_FLIGHT(DATE(scheduled_departure));

-- FT_PASSENGER indexes
CREATE INDEX idx_ft_passenger_ingestion_time ON FT_PASSENGER(ingestion_time);
CREATE INDEX idx_ft_passenger_processed ON FT_PASSENGER(is_processed);

-- FT_BOOKING indexes
CREATE INDEX idx_ft_booking_ingestion_time ON FT_BOOKING(ingestion_time);
CREATE INDEX idx_ft_booking_processed ON FT_BOOKING(is_processed);
CREATE INDEX idx_ft_booking_passenger_id ON FT_BOOKING(passenger_id);
CREATE INDEX idx_ft_booking_flight_id ON FT_BOOKING(flight_id);

-- FT_MAINTENANCE_EVENT indexes
CREATE INDEX idx_ft_maintenance_ingestion_time ON FT_MAINTENANCE_EVENT(ingestion_time);
CREATE INDEX idx_ft_maintenance_processed ON FT_MAINTENANCE_EVENT(is_processed);
CREATE INDEX idx_ft_maintenance_aircraft_id ON FT_MAINTENANCE_EVENT(aircraft_id);

-- FT_CREW_ASSIGNMENT indexes
CREATE INDEX idx_ft_crew_ingestion_time ON FT_CREW_ASSIGNMENT(ingestion_time);
CREATE INDEX idx_ft_crew_processed ON FT_CREW_ASSIGNMENT(is_processed);
CREATE INDEX idx_ft_crew_flight_id ON FT_CREW_ASSIGNMENT(flight_id);

-- FT_BAGGAGE indexes
CREATE INDEX idx_ft_baggage_ingestion_time ON FT_BAGGAGE(ingestion_time);
CREATE INDEX idx_ft_baggage_processed ON FT_BAGGAGE(is_processed);
CREATE INDEX idx_ft_baggage_booking_id ON FT_BAGGAGE(booking_id);
-- bag_tag kolonu yok, bu index'i kaldırıyoruz

-- FT_PASSENGER_FEEDBACK indexes
CREATE INDEX idx_ft_feedback_ingestion_time ON FT_PASSENGER_FEEDBACK(ingestion_time);
CREATE INDEX idx_ft_feedback_processed ON FT_PASSENGER_FEEDBACK(is_processed);
CREATE INDEX idx_ft_feedback_passenger_id ON FT_PASSENGER_FEEDBACK(passenger_id);
CREATE INDEX idx_ft_feedback_flight_id ON FT_PASSENGER_FEEDBACK(flight_id);

-- FT_PASSENGER_NOTIFICATION indexes
CREATE INDEX idx_ft_notification_ingestion_time ON FT_PASSENGER_NOTIFICATION(ingestion_time);
CREATE INDEX idx_ft_notification_processed ON FT_PASSENGER_NOTIFICATION(is_processed);
CREATE INDEX idx_ft_notification_passenger_id ON FT_PASSENGER_NOTIFICATION(passenger_id);

-- FT_FLIGHT_INCIDENT indexes
CREATE INDEX idx_ft_incident_ingestion_time ON FT_FLIGHT_INCIDENT(ingestion_time);
CREATE INDEX idx_ft_incident_processed ON FT_FLIGHT_INCIDENT(is_processed);
CREATE INDEX idx_ft_incident_flight_id ON FT_FLIGHT_INCIDENT(flight_id);

-- FT_FLIGHT_FUEL indexes
CREATE INDEX idx_ft_fuel_ingestion_time ON FT_FLIGHT_FUEL(ingestion_time);
CREATE INDEX idx_ft_fuel_processed ON FT_FLIGHT_FUEL(is_processed);
CREATE INDEX idx_ft_fuel_flight_id ON FT_FLIGHT_FUEL(flight_id);


COMMENT ON TABLE FT_FLIGHT IS 'Raw flight data from operational systems';
COMMENT ON TABLE FT_PASSENGER IS 'Raw passenger data from booking and check-in systems';
COMMENT ON TABLE FT_BOOKING IS 'Raw booking and reservation data';
COMMENT ON TABLE FT_MAINTENANCE_EVENT IS 'Raw aircraft maintenance records';
COMMENT ON TABLE FT_CREW_ASSIGNMENT IS 'Raw crew assignment and duty records';
COMMENT ON TABLE FT_BAGGAGE IS 'Raw baggage tracking and handling data';
COMMENT ON TABLE FT_PASSENGER_FEEDBACK IS 'Raw customer feedback and survey data';

-- =====================================
-- TR (TRANSACTIONAL REPORTING) TABLES
-- =====================================
-- These are reporting views and summary tables built from FT tables

-- Remove old TR views and use actual tables
-- Note: These might be tables or views, so we handle both cases
DO $$
BEGIN
    -- Check and drop if VIEW exists
    IF EXISTS (SELECT 1 FROM information_schema.views WHERE table_name = 'tr_flight') THEN
        DROP VIEW tr_flight CASCADE;
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.views WHERE table_name = 'tr_booking') THEN
        DROP VIEW tr_booking CASCADE;
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.views WHERE table_name = 'tr_passenger') THEN
        DROP VIEW tr_passenger CASCADE;
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.views WHERE table_name = 'tr_crew_assignment') THEN
        DROP VIEW tr_crew_assignment CASCADE;
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.views WHERE table_name = 'tr_flight_fuel') THEN
        DROP VIEW tr_flight_fuel CASCADE;
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.views WHERE table_name = 'tr_maintenance_event') THEN
        DROP VIEW tr_maintenance_event CASCADE;
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.views WHERE table_name = 'tr_baggage') THEN
        DROP VIEW tr_baggage CASCADE;
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.views WHERE table_name = 'tr_passenger_notification') THEN
        DROP VIEW tr_passenger_notification CASCADE;
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.views WHERE table_name = 'tr_flight_incident') THEN
        DROP VIEW tr_flight_incident CASCADE;
    END IF;
END $$;

-- Update existing TR tables to have proper structure
-- tr_flight already exists as table, just need to ensure it has right columns
ALTER TABLE tr_flight ADD COLUMN IF NOT EXISTS delay_minutes NUMERIC;
ALTER TABLE tr_flight ADD COLUMN IF NOT EXISTS is_ontime BOOLEAN;
ALTER TABLE tr_flight ADD COLUMN IF NOT EXISTS day_of_week INTEGER;
ALTER TABLE tr_flight ADD COLUMN IF NOT EXISTS departure_hour INTEGER;

-- Update tr_booking table
ALTER TABLE tr_booking ADD COLUMN IF NOT EXISTS days_since_registration NUMERIC;
ALTER TABLE tr_booking ADD COLUMN IF NOT EXISTS is_same_day_booking BOOLEAN;
ALTER TABLE tr_booking ADD COLUMN IF NOT EXISTS price_per_km NUMERIC;

-- Update tr_passenger table  
ALTER TABLE tr_passenger ADD COLUMN IF NOT EXISTS age INTEGER;
ALTER TABLE tr_passenger ADD COLUMN IF NOT EXISTS total_flights INTEGER;
ALTER TABLE tr_passenger ADD COLUMN IF NOT EXISTS total_spent NUMERIC;
ALTER TABLE tr_passenger ADD COLUMN IF NOT EXISTS days_since_registration NUMERIC;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_tr_flight_scheduled_departure ON tr_flight(scheduled_departure);
CREATE INDEX IF NOT EXISTS idx_tr_booking_booking_date ON tr_booking(booking_date);
CREATE INDEX IF NOT EXISTS idx_tr_passenger_registration_date ON tr_passenger(registration_date);
CREATE INDEX IF NOT EXISTS idx_tr_crew_shift_start ON tr_crew_assignment(shift_start);
CREATE INDEX IF NOT EXISTS idx_tr_maintenance_event_time ON tr_maintenance_event(event_time);
CREATE INDEX IF NOT EXISTS idx_etl_log_procedure ON etl_procedure_log(procedure_name, started_at);

-- Grant permissions
GRANT SELECT ON ALL TABLES IN SCHEMA public TO public;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO public;
GRANT INSERT, UPDATE, DELETE ON etl_procedure_log TO public;
