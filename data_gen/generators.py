import uuid
import random
from datetime import datetime, timedelta
from faker import Faker
from typing import List, Dict, Optional

fake = Faker()

# Sabitler ve örnek lookup verileri
def get_airports(n=30) -> List[str]:
    return [fake.unique.bothify(text='???') for _ in range(n)]

def get_countries(n=20) -> List[str]:
    return [fake.country() for _ in range(n)]

def get_aircraft_ids(n=50) -> List[str]:
    return [str(uuid.uuid4()) for _ in range(n)]

LOYALTY_TIERS = ['Bronze', 'Silver', 'Gold', 'Platinum']
FLIGHT_STATUSES = ['Scheduled', 'Delayed', 'Cancelled', 'Completed']
WEATHER_CONDITIONS = ['Clear', 'Rain', 'Fog', 'Storm', 'Snow']
DELAY_REASONS = ['Weather', 'Technical', 'Crew', 'ATC', 'None']
CANCELLATION_REASONS = ['Weather', 'Technical', 'Crew', 'ATC', 'None']

# FT_FLIGHT veri üretimi
def generate_ft_flight(n: int = 100) -> List[Dict]:
    airports = get_airports()
    countries = get_countries()
    aircraft_ids = get_aircraft_ids()
    flights = []
    for _ in range(n):
        departure_airport, arrival_airport = random.sample(airports, 2)
        scheduled_departure = fake.date_time_between(start_date='-30d', end_date='+30d')
        actual_departure = scheduled_departure + timedelta(minutes=random.randint(-10, 180)) if random.random() > 0.1 else None
        status = random.choice(FLIGHT_STATUSES)
        is_international = random.choice([True, False])
        origin_country = random.choice(countries)
        destination_country = random.choice([c for c in countries if c != origin_country])
        distance_km = round(random.uniform(300, 9000), 1)
        duration_min = int(distance_km / random.uniform(8, 13))
        flights.append({
            "flight_id": str(uuid.uuid4()),
            "flight_number": fake.bothify(text='SW###'),
            "departure_airport": departure_airport,
            "arrival_airport": arrival_airport,
            "scheduled_departure": scheduled_departure.isoformat(),
            "actual_departure": actual_departure.isoformat() if actual_departure else None,
            "aircraft_id": random.choice(aircraft_ids),
            "flight_status": status,
            "weather_condition": random.choice(WEATHER_CONDITIONS),
            "cancellation_reason": random.choice(CANCELLATION_REASONS) if status == 'Cancelled' else None,
            "delay_reason": random.choice(DELAY_REASONS) if status == 'Delayed' else None,
            "origin_country": origin_country,
            "destination_country": destination_country,
            "distance_km": distance_km,
            "flight_duration_min": duration_min,
            "is_international": is_international,
            "gate_number": fake.bothify(text='G##'),
            "created_at": datetime.now().isoformat()
        })
    return flights

# FT_PASSENGER veri üretimi
def generate_ft_passenger(n: int = 500) -> List[Dict]:
    countries = get_countries()
    passengers = []
    for _ in range(n):
        gender = random.choice(['Male', 'Female', 'Other'])
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=85)
        registration_date = fake.date_between(start_date='-5y', end_date='today')
        passengers.append({
            "passenger_id": str(uuid.uuid4()),
            "full_name": fake.name_male() if gender == 'Male' else fake.name_female() if gender == 'Female' else fake.name(),
            "birth_date": birth_date.isoformat(),
            "nationality": random.choice(countries),
            "frequent_flyer": random.choice([True, False]),
            "loyalty_tier": random.choice(LOYALTY_TIERS),
            "email": fake.unique.email(),
            "phone_number": fake.phone_number(),
            "gender": gender,
            "registration_date": registration_date.isoformat(),
            "passport_number": fake.bothify(text='P########'),
            "created_at": datetime.now().isoformat()
        })
    return passengers

def generate_ft_booking(n: int = 300, passenger_ids=None, flight_ids=None) -> List[Dict]:
    if passenger_ids is None:
        passenger_ids = [str(uuid.uuid4()) for _ in range(n)]
    if flight_ids is None:
        flight_ids = [str(uuid.uuid4()) for _ in range(n)]
    bookings = []
    for _ in range(n):
        passenger_id = random.choice(passenger_ids)
        flight_id = random.choice(flight_ids)
        booking_date = fake.date_time_between(start_date='-30d', end_date='+30d')
        cancel = random.random() < 0.1
        cancel_date = booking_date + timedelta(days=random.randint(0, 10)) if cancel else None
        bookings.append({
            "booking_id": str(uuid.uuid4()),
            "passenger_id": passenger_id,
            "flight_id": flight_id,
            "booking_date": booking_date.isoformat(),
            "cancel_date": cancel_date.isoformat() if cancel_date else None,
            "is_cancelled": cancel,
            "fare_class": random.choice(['Economy', 'Business', 'First']),
            "ticket_price": round(random.uniform(50, 2000), 2),
            "seat_number": fake.bothify(text='##A'),
            "booking_channel": random.choice(['Website', 'Mobile', 'Agent']),
            "payment_method": random.choice(['Credit Card', 'Miles', 'Voucher']),
            "currency": random.choice(['USD', 'EUR', 'TRY']),
            "discount_applied": random.choice([True, False]),
            "promo_code": fake.bothify(text='PROMO####') if random.random() < 0.2 else None,
            "created_at": datetime.now().isoformat()
        })
    return bookings

def generate_ft_baggage(n: int = 300, booking_ids=None) -> List[Dict]:
    if booking_ids is None:
        booking_ids = [str(uuid.uuid4()) for _ in range(n)]
    bag_types = ['Checked', 'Carry-on']
    bag_statuses = ['Loaded', 'Lost', 'Damaged', 'Delivered']
    baggages = []
    for _ in range(n):
        baggages.append({
            "baggage_id": str(uuid.uuid4()),
            "booking_id": random.choice(booking_ids),
            "baggage_type": random.choice(bag_types),
            "weight_kg": round(random.uniform(5, 32), 1),
            "is_special_handling": random.choice([True, False]),
            "baggage_status": random.choice(bag_statuses),
            "created_at": datetime.now().isoformat()
        })
    return baggages

def generate_ft_crew_assignment(n: int = 100, flight_ids=None) -> List[Dict]:
    if flight_ids is None:
        flight_ids = [str(uuid.uuid4()) for _ in range(n)]
    crew_ids = [str(uuid.uuid4()) for _ in range(n*2)]
    roles = ['Pilot', 'Attendant', 'Engineer']
    assignment_statuses = ['Confirmed', 'Pending', 'Cancelled']
    assignments = []
    for _ in range(n):
        shift_start = fake.date_time_between(start_date='-30d', end_date='+30d')
        shift_end = shift_start + timedelta(hours=random.randint(2, 12))
        assignments.append({
            "assignment_id": str(uuid.uuid4()),
            "flight_id": random.choice(flight_ids),
            "crew_id": random.choice(crew_ids),
            "role": random.choice(roles),
            "shift_start": shift_start.isoformat(),
            "shift_end": shift_end.isoformat(),
            "is_lead": random.choice([True, False]),
            "assignment_status": random.choice(assignment_statuses),
            "created_at": datetime.now().isoformat()
        })
    return assignments

def generate_ft_passenger_notification(n: int = 200, passenger_ids=None, flight_ids=None) -> List[Dict]:
    if passenger_ids is None:
        passenger_ids = [str(uuid.uuid4()) for _ in range(n)]
    if flight_ids is None:
        flight_ids = [str(uuid.uuid4()) for _ in range(n)]
    notif_types = ['Delay', 'Cancel', 'Promo']
    delivery_channels = ['SMS', 'EMAIL', 'PUSH']
    delivery_statuses = ['Sent', 'Failed', 'Pending']
    notifications = []
    for _ in range(n):
        notifications.append({
            "notification_id": str(uuid.uuid4()),
            "passenger_id": random.choice(passenger_ids),
            "flight_id": random.choice(flight_ids) if random.random() > 0.2 else None,
            "notification_type": random.choice(notif_types),
            "message_content": fake.sentence(),
            "send_time": fake.date_time_between(start_date='-30d', end_date='+30d').isoformat(),
            "delivery_channel": random.choice(delivery_channels),
            "delivery_status": random.choice(delivery_statuses),
            "read_status": random.choice([True, False]),
            "created_at": datetime.now().isoformat()
        })
    return notifications

def generate_ft_flight_incident(n: int = 30, flight_ids=None) -> List[Dict]:
    if flight_ids is None:
        flight_ids = [str(uuid.uuid4()) for _ in range(n)]
    incident_types = ['Medical', 'Technical', 'Security']
    severities = ['Low', 'Medium', 'High']
    incidents = []
    for _ in range(n):
        reported_time = fake.date_time_between(start_date='-30d', end_date='+30d')
        resolved_time = reported_time + timedelta(hours=random.randint(1, 24))
        incidents.append({
            "incident_id": str(uuid.uuid4()),
            "flight_id": random.choice(flight_ids),
            "incident_type": random.choice(incident_types),
            "description": fake.sentence(),
            "reported_time": reported_time.isoformat(),
            "resolved_time": resolved_time.isoformat(),
            "severity": random.choice(severities),
            "created_at": datetime.now().isoformat()
        })
    return incidents

def generate_ft_passenger_feedback(n: int = 100, passenger_ids=None, flight_ids=None) -> List[Dict]:
    if passenger_ids is None:
        passenger_ids = [str(uuid.uuid4()) for _ in range(n)]
    if flight_ids is None:
        flight_ids = [str(uuid.uuid4()) for _ in range(n)]
    feedback_types = ['Complaint', 'Praise', 'Suggestion']
    feedbacks = []
    for _ in range(n):
        feedbacks.append({
            "feedback_id": str(uuid.uuid4()),
            "passenger_id": random.choice(passenger_ids),
            "flight_id": random.choice(flight_ids),
            "feedback_type": random.choice(feedback_types),
            "feedback_text": fake.sentence(),
            "rating": random.randint(1, 5),
            "submitted_at": fake.date_time_between(start_date='-30d', end_date='+30d').isoformat(),
            "created_at": datetime.now().isoformat()
        })
    return feedbacks

def generate_ft_flight_fuel(n: int = 50, flight_ids=None) -> List[Dict]:
    if flight_ids is None:
        flight_ids = [str(uuid.uuid4()) for _ in range(n)]
    fuel_types = ['Jet A', 'Jet A-1', 'Avgas']
    fuels = []
    for _ in range(n):
        fueling_time = fake.date_time_between(start_date='-30d', end_date='+30d')
        fuels.append({
            "fuel_id": str(uuid.uuid4()),
            "flight_id": random.choice(flight_ids),
            "fuel_type": random.choice(fuel_types),
            "fuel_quantity_liters": round(random.uniform(1000, 20000), 1),
            "fueling_time": fueling_time.isoformat(),
            "fueling_company": fake.company(),
            "created_at": datetime.now().isoformat()
        })
    return fuels

def generate_ft_maintenance_event(n: int = 20, aircraft_ids=None) -> List[Dict]:
    if aircraft_ids is None:
        aircraft_ids = [str(uuid.uuid4()) for _ in range(n)]
    event_types = ['Scheduled', 'Unscheduled']
    events = []
    for _ in range(n):
        event_time = fake.date_time_between(start_date='-30d', end_date='+30d')
        resolved_time = event_time + timedelta(hours=random.randint(1, 48))
        events.append({
            "maintenance_id": str(uuid.uuid4()),
            "aircraft_id": random.choice(aircraft_ids),
            "event_type": random.choice(event_types),
            "description": fake.sentence(),
            "event_time": event_time.isoformat(),
            "resolved_time": resolved_time.isoformat(),
            "cost": round(random.uniform(1000, 100000), 2),
            "created_at": datetime.now().isoformat()
        })
    return events 