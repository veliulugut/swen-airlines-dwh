-- =================================================================
-- Swen Airlines DWH - FT (Fact Table) Tabloları (Güncel Şema)
-- =================================================================

-- Gerekirse eski tabloları sil
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

-- =================================================================
-- FT_FLIGHT
-- =================================================================
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

-- =================================================================
-- FT_PASSENGER
-- =================================================================
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

-- =================================================================
-- FT_BOOKING
-- =================================================================
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

-- =================================================================
-- FT_BAGGAGE
-- =================================================================
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

-- =================================================================
-- FT_CREW_ASSIGNMENT
-- =================================================================
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

-- =================================================================
-- FT_PASSENGER_NOTIFICATION
-- =================================================================
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

-- =================================================================
-- FT_FLIGHT_INCIDENT
-- =================================================================
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

-- =================================================================
-- FT_PASSENGER_FEEDBACK
-- =================================================================
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

-- =================================================================
-- FT_FLIGHT_FUEL
-- =================================================================
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

-- =================================================================
-- FT_MAINTENANCE_EVENT
-- =================================================================
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

-- =================================================================
-- Indexes for FT Tables (Performance optimization)
-- =================================================================

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

-- FT_AIRCRAFT_MAINTENANCE indexes
CREATE INDEX idx_ft_maintenance_ingestion_time ON FT_AIRCRAFT_MAINTENANCE(ingestion_time);
CREATE INDEX idx_ft_maintenance_processed ON FT_AIRCRAFT_MAINTENANCE(is_processed);
CREATE INDEX idx_ft_maintenance_aircraft_id ON FT_AIRCRAFT_MAINTENANCE(aircraft_id);

-- FT_CREW_ASSIGNMENT indexes
CREATE INDEX idx_ft_crew_ingestion_time ON FT_CREW_ASSIGNMENT(ingestion_time);
CREATE INDEX idx_ft_crew_processed ON FT_CREW_ASSIGNMENT(is_processed);
CREATE INDEX idx_ft_crew_flight_id ON FT_CREW_ASSIGNMENT(flight_id);

-- FT_BAGGAGE indexes
CREATE INDEX idx_ft_baggage_ingestion_time ON FT_BAGGAGE(ingestion_time);
CREATE INDEX idx_ft_baggage_processed ON FT_BAGGAGE(is_processed);
CREATE INDEX idx_ft_baggage_booking_id ON FT_BAGGAGE(booking_id);
CREATE INDEX idx_ft_baggage_tag ON FT_BAGGAGE(bag_tag);

-- FT_CUSTOMER_FEEDBACK indexes
CREATE INDEX idx_ft_feedback_ingestion_time ON FT_CUSTOMER_FEEDBACK(ingestion_time);
CREATE INDEX idx_ft_feedback_processed ON FT_CUSTOMER_FEEDBACK(is_processed);
CREATE INDEX idx_ft_feedback_passenger_id ON FT_CUSTOMER_FEEDBACK(passenger_id);
CREATE INDEX idx_ft_feedback_flight_id ON FT_CUSTOMER_FEEDBACK(flight_id);

-- =================================================================
-- Comments for documentation
-- =================================================================
COMMENT ON TABLE FT_FLIGHT IS 'Raw flight data from operational systems';
COMMENT ON TABLE FT_PASSENGER IS 'Raw passenger data from booking and check-in systems';
COMMENT ON TABLE FT_BOOKING IS 'Raw booking and reservation data';
COMMENT ON TABLE FT_AIRCRAFT_MAINTENANCE IS 'Raw aircraft maintenance records';
COMMENT ON TABLE FT_CREW_ASSIGNMENT IS 'Raw crew assignment and duty records';
COMMENT ON TABLE FT_BAGGAGE IS 'Raw baggage tracking and handling data';
COMMENT ON TABLE FT_CUSTOMER_FEEDBACK IS 'Raw customer feedback and survey data';
