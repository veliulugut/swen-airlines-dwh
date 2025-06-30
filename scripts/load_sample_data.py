#!/usr/bin/env python3
"""
Automatic Sample Data Loader for Swen Airlines DWH
This script populates FT tables with realistic sample data
"""

import psycopg2
import uuid
from datetime import datetime, timedelta
import random
import time
import sys

# Database configuration
DB_CONFIG = {
    'host': 'postgres',
    'port': 5432,
    'database': 'swen_dwh',
    'user': 'admin',
    'password': 'admin'
}

def wait_for_db():
    """Wait for database to be ready"""
    print("🔄 Waiting for PostgreSQL to be ready...")
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            conn.close()
            print("✅ PostgreSQL is ready!")
            return True
        except psycopg2.OperationalError:
            retry_count += 1
            print(f"⏳ Attempt {retry_count}/{max_retries} - Database not ready yet...")
            time.sleep(2)
    
    print("❌ Failed to connect to database after 30 attempts")
    return False

def load_sample_data():
    """Load comprehensive sample data into FT tables"""
    if not wait_for_db():
        sys.exit(1)
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("🚀 Starting sample data loading...")
        
        # Sample data
        airports = ['IST', 'SAW', 'ESB', 'ADB', 'AYT', 'BJV', 'TZX', 'GZT']
        countries = ['Turkey', 'Germany', 'France', 'UK', 'Spain', 'Italy']
        flight_statuses = ['Scheduled', 'Delayed', 'Cancelled', 'Completed']
        fare_classes = ['Economy', 'Business', 'First']
        channels = ['Website', 'Mobile', 'Agent', 'Call Center']
        
        # 1. Load Aircraft data (referenced by flights)
        aircraft_ids = []
        for i in range(20):
            aircraft_id = str(uuid.uuid4())
            aircraft_ids.append(aircraft_id)
        
        # 2. Load Passengers
        print("👥 Loading passengers...")
        passenger_ids = []
        for i in range(200):
            passenger_id = str(uuid.uuid4())
            passenger_ids.append(passenger_id)
            
            cursor.execute("""
                INSERT INTO ft_passenger (
                    passenger_id, full_name, birth_date, nationality, frequent_flyer,
                    loyalty_tier, email, phone_number, gender, registration_date, passport_number
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                passenger_id,
                f"Passenger {i+1}",
                datetime.now().date() - timedelta(days=random.randint(6570, 25550)),  # Age 18-70
                random.choice(countries),
                random.choice([True, False]),
                random.choice(['Bronze', 'Silver', 'Gold', 'Platinum']) if random.random() > 0.3 else None,
                f"passenger{i+1}@email.com",
                f"+90{random.randint(5000000000, 5999999999)}",
                random.choice(['M', 'F']),
                datetime.now().date() - timedelta(days=random.randint(1, 365)),
                f"P{random.randint(10000000, 99999999)}"
            ))
        
        # 3. Load Flights
        print("✈️ Loading flights...")
        flight_ids = []
        for i in range(100):
            flight_id = str(uuid.uuid4())
            flight_ids.append(flight_id)
            
            departure_time = datetime.now() - timedelta(days=random.randint(0, 30)) + timedelta(hours=random.randint(0, 23))
            actual_departure = departure_time + timedelta(minutes=random.randint(-10, 120)) if random.random() > 0.2 else None
            
            cursor.execute("""
                INSERT INTO ft_flight (
                    flight_id, flight_number, departure_airport, arrival_airport,
                    scheduled_departure, actual_departure, aircraft_id, flight_status,
                    weather_condition, origin_country, destination_country,
                    distance_km, flight_duration_min, is_international, gate_number
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                flight_id,
                f"SW{1000 + i}",
                random.choice(airports),
                random.choice(airports),
                departure_time,
                actual_departure,
                random.choice(aircraft_ids),
                random.choice(flight_statuses),
                random.choice(['Clear', 'Cloudy', 'Rainy', 'Stormy']),
                random.choice(countries),
                random.choice(countries),
                random.uniform(200, 3000),
                random.randint(60, 600),
                random.choice([True, False]),
                f"A{random.randint(1, 50)}"
            ))
        
        # 4. Load Bookings
        print("🎫 Loading bookings...")
        booking_ids = []
        for i in range(150):
            booking_id = str(uuid.uuid4())
            booking_ids.append(booking_id)
            
            booking_date = datetime.now() - timedelta(days=random.randint(1, 60))
            
            cursor.execute("""
                INSERT INTO ft_booking (
                    booking_id, passenger_id, flight_id, booking_date, is_cancelled,
                    fare_class, ticket_price, seat_number, booking_channel,
                    payment_method, currency, discount_applied, promo_code
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                booking_id,
                random.choice(passenger_ids),
                random.choice(flight_ids),
                booking_date,
                random.choice([True, False]) if random.random() < 0.1 else False,
                random.choice(fare_classes),
                random.uniform(200, 2000),
                f"{random.randint(1, 30)}{random.choice(['A', 'B', 'C', 'D', 'E', 'F'])}",
                random.choice(channels),
                random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer']),
                'TRY',
                random.choice([True, False]),
                f"PROMO{random.randint(100, 999)}" if random.random() < 0.3 else None
            ))
        
        # 5. Load Crew Assignments
        print("👨‍✈️ Loading crew assignments...")
        crew_ids = [str(uuid.uuid4()) for _ in range(50)]
        for i in range(80):
            cursor.execute("""
                INSERT INTO ft_crew_assignment (
                    assignment_id, flight_id, crew_id, role,
                    shift_start, shift_end, is_lead, assignment_status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()),
                random.choice(flight_ids),
                random.choice(crew_ids),
                random.choice(['Pilot', 'Co-Pilot', 'Flight Attendant', 'Engineer']),
                datetime.now() - timedelta(hours=random.randint(1, 168)),
                datetime.now() - timedelta(hours=random.randint(1, 160)),
                random.choice([True, False]),
                random.choice(['Confirmed', 'Pending', 'Cancelled'])
            ))
        
        # 6. Load Baggage
        print("🧳 Loading baggage...")
        for i in range(120):
            cursor.execute("""
                INSERT INTO ft_baggage (
                    baggage_id, booking_id, baggage_type, weight_kg,
                    is_special_handling, baggage_status
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()),
                random.choice(booking_ids),
                random.choice(['Checked', 'Carry-on']),
                random.uniform(2, 25),
                random.choice([True, False]),
                random.choice(['Loaded', 'Lost', 'Damaged', 'Delivered'])
            ))
        
        # 7. Load Flight Fuel
        print("⛽ Loading flight fuel...")
        for i in range(90):
            cursor.execute("""
                INSERT INTO ft_flight_fuel (
                    fuel_id, flight_id, fuel_type, fuel_quantity_liters,
                    fueling_time, fueling_company
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()),
                random.choice(flight_ids),
                random.choice(['Jet A-1', 'Jet A', 'TS-1']),
                random.uniform(5000, 15000),
                datetime.now() - timedelta(hours=random.randint(1, 720)),
                random.choice(['Shell', 'BP', 'TotalEnergies', 'Petrol Ofisi'])
            ))
        
        # 8. Load Maintenance Events  
        print("🔧 Loading maintenance events...")
        for i in range(60):
            cursor.execute("""
                INSERT INTO ft_maintenance_event (
                    maintenance_id, aircraft_id, event_type, description,
                    event_time, resolved_time, cost
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()),
                random.choice(aircraft_ids),
                random.choice(['Scheduled', 'Unscheduled']),
                f"Maintenance Event {i+1}",
                datetime.now() - timedelta(hours=random.randint(1, 2160)),
                datetime.now() - timedelta(hours=random.randint(1, 2150)),
                random.uniform(1000, 50000)
            ))
        
        # 9. Load Flight Incidents
        print("⚠️ Loading flight incidents...")
        for i in range(30):
            cursor.execute("""
                INSERT INTO ft_flight_incident (
                    incident_id, flight_id, incident_type, description,
                    reported_time, resolved_time, severity
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()),
                random.choice(flight_ids),
                random.choice(['Medical', 'Technical', 'Security', 'Weather']),
                f"Incident {i+1}",
                datetime.now() - timedelta(hours=random.randint(1, 720)),
                datetime.now() - timedelta(hours=random.randint(1, 700)),
                random.choice(['Low', 'Medium', 'High'])
            ))
        
        # 10. Load Passenger Notifications
        print("📱 Loading passenger notifications...")
        for i in range(100):
            cursor.execute("""
                INSERT INTO ft_passenger_notification (
                    notification_id, passenger_id, flight_id, notification_type,
                    message_content, send_time, delivery_channel, delivery_status, read_status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()),
                random.choice(passenger_ids),
                random.choice(flight_ids) if random.random() > 0.3 else None,
                random.choice(['Delay', 'Gate Change', 'Boarding', 'Cancellation', 'Promotion']),
                f"Notification message {i+1}",
                datetime.now() - timedelta(hours=random.randint(1, 168)),
                random.choice(['SMS', 'EMAIL', 'PUSH']),
                random.choice(['Sent', 'Failed', 'Pending']),
                random.choice([True, False])
            ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Sample data loading completed successfully!")
        print(f"📊 Loaded:")
        print(f"   - {len(passenger_ids)} passengers")
        print(f"   - {len(flight_ids)} flights")
        print(f"   - {len(booking_ids)} bookings")
        print(f"   - 80 crew assignments")
        print(f"   - 120 baggage records")
        print(f"   - 90 fuel records")
        print(f"   - 60 maintenance events")
        print(f"   - 30 flight incidents")
        print(f"   - 100 passenger notifications")
        
    except Exception as e:
        print(f"❌ Error loading sample data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    load_sample_data() 