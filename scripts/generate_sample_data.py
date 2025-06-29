#!/usr/bin/env python3
"""
Generate sample data directly to PostgreSQL
"""
import psycopg2
from datetime import datetime, timedelta
import uuid
import random
from faker import Faker

fake = Faker()

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="swen_dwh",
        user="admin",
        password="admin"
    )

def generate_flight_data(num_records=100):
    """Generate sample flight data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    airports = ['JFK', 'LAX', 'LHR', 'CDG', 'FRA', 'NRT', 'DXB', 'SIN', 'IST', 'AMS']
    statuses = ['Scheduled', 'Delayed', 'Cancelled', 'Completed']
    
    print(f"🛫 Generating {num_records} flight records...")
    
    for i in range(num_records):
        flight_id = str(uuid.uuid4())
        departure_airport = random.choice(airports)
        arrival_airport = random.choice([a for a in airports if a != departure_airport])
        
        # Random departure time in last 30 days
        scheduled_departure = fake.date_time_between(start_date='-30d', end_date='now')
        actual_departure = scheduled_departure + timedelta(minutes=random.randint(-30, 120))
        
        flight_number = f"SW{random.randint(100, 999)}"
        aircraft_id = str(uuid.uuid4())
        flight_status = random.choice(statuses)
        distance_km = random.randint(200, 8000)
        duration_min = random.randint(60, 600)
        is_international = departure_airport != arrival_airport
        
        cursor.execute("""
            INSERT INTO ft_flight (
                flight_id, flight_number, departure_airport, arrival_airport,
                scheduled_departure, actual_departure, aircraft_id, flight_status,
                weather_condition, origin_country, destination_country,
                distance_km, flight_duration_min, is_international, gate_number
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            flight_id, flight_number, departure_airport, arrival_airport,
            scheduled_departure, actual_departure, aircraft_id, flight_status,
            random.choice(['Clear', 'Cloudy', 'Rainy', 'Stormy']),
            random.choice(['US', 'UK', 'FR', 'DE', 'JP']),
            random.choice(['US', 'UK', 'FR', 'DE', 'JP']),
            distance_km, duration_min, is_international,
            f"A{random.randint(1, 50)}"
        ))
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Generated {num_records} flight records")

def generate_passenger_data(num_records=500):
    """Generate sample passenger data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print(f"👤 Generating {num_records} passenger records...")
    
    for i in range(num_records):
        passenger_id = str(uuid.uuid4())
        full_name = fake.name()
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=80)
        nationality = random.choice(['US', 'UK', 'FR', 'DE', 'JP', 'CA', 'AU'])
        frequent_flyer = random.choice([True, False])
        loyalty_tier = random.choice(['Bronze', 'Silver', 'Gold', 'Platinum']) if frequent_flyer else None
        email = fake.email()
        phone = fake.phone_number()
        gender = random.choice(['M', 'F'])
        registration_date = fake.date_between(start_date='-2y', end_date='today')
        passport_number = fake.passport_number()
        
        cursor.execute("""
            INSERT INTO ft_passenger (
                passenger_id, full_name, birth_date, nationality, frequent_flyer,
                loyalty_tier, email, phone_number, gender, registration_date, passport_number
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            passenger_id, full_name, birth_date, nationality, frequent_flyer,
            loyalty_tier, email, phone, gender, registration_date, passport_number
        ))
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Generated {num_records} passenger records")

def generate_booking_data(num_records=300):
    """Generate sample booking data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get existing passengers and flights
    cursor.execute("SELECT passenger_id FROM ft_passenger LIMIT 100")
    passengers = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT flight_id FROM ft_flight LIMIT 100") 
    flights = [row[0] for row in cursor.fetchall()]
    
    if not passengers or not flights:
        print("❌ No passengers or flights found. Generate those first.")
        return
    
    print(f"🎫 Generating {num_records} booking records...")
    
    for i in range(num_records):
        booking_id = str(uuid.uuid4())
        passenger_id = random.choice(passengers)
        flight_id = random.choice(flights)
        booking_date = fake.date_time_between(start_date='-30d', end_date='now')
        is_cancelled = random.choice([True, False])
        cancel_date = booking_date + timedelta(days=random.randint(1, 10)) if is_cancelled else None
        fare_class = random.choice(['Economy', 'Business', 'First'])
        ticket_price = random.randint(100, 2000)
        seat_number = f"{random.randint(1, 30)}{random.choice(['A', 'B', 'C', 'D', 'E', 'F'])}"
        booking_channel = random.choice(['Website', 'Mobile', 'Agent'])
        payment_method = random.choice(['Credit Card', 'Miles', 'Voucher'])
        currency = random.choice(['USD', 'EUR', 'GBP'])
        
        cursor.execute("""
            INSERT INTO ft_booking (
                booking_id, passenger_id, flight_id, booking_date, cancel_date,
                is_cancelled, fare_class, ticket_price, seat_number, booking_channel,
                payment_method, currency, discount_applied
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            booking_id, passenger_id, flight_id, booking_date, cancel_date,
            is_cancelled, fare_class, ticket_price, seat_number, booking_channel,
            payment_method, currency, random.choice([True, False])
        ))
    
    conn.commit()
    cursor.close() 
    conn.close()
    print(f"✅ Generated {num_records} booking records")

def run_procedures():
    """Run all procedures to populate TR tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    procedures = [
        'job_flight',
        'job_passenger', 
        'job_booking'
    ]
    
    print("🔄 Running procedures to populate TR tables...")
    
    for proc in procedures:
        try:
            print(f"  📊 Running {proc}...")
            cursor.execute(f"CALL {proc}('full');")
            conn.commit()
            print(f"  ✅ {proc} completed")
        except Exception as e:
            print(f"  ❌ Error in {proc}: {e}")
    
    cursor.close()
    conn.close()

def main():
    print("🎲 SAMPLE DATA GENERATOR 🎲")
    print("=" * 50)
    
    try:
        # Generate base data
        generate_flight_data(100)
        generate_passenger_data(500)
        generate_booking_data(300)
        
        # Run procedures
        run_procedures()
        
        print("=" * 50)
        print("🎉 Sample data generation completed!")
        print("📊 You can now view data in the dashboard at http://localhost:8501")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 