#!/usr/bin/env python3
"""
Test script for stored procedures
"""
import psycopg2
import time
from datetime import datetime

# Database connection
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="swen_dwh",
        user="admin",
        password="admin"
    )

def test_procedure(proc_name):
    """Test a specific procedure"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print(f"🔄 Testing procedure: {proc_name}")
        start_time = datetime.now()
        
        # Call procedure
        cursor.execute(f"CALL {proc_name}('delta');")
        conn.commit()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"✅ {proc_name} completed successfully in {duration:.2f} seconds")
        
        # Check row count in target TR table
        tr_table = f"tr_{proc_name.replace('job_', '')}"
        cursor.execute(f"SELECT COUNT(*) FROM {tr_table};")
        count = cursor.fetchone()[0]
        print(f"   📊 {tr_table} has {count} rows")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error in {proc_name}: {str(e)}")
        return False

def main():
    print("🧪 PROSEDÜR TEST ARACІ 🧪")
    print("=" * 50)
    
    procedures = [
        'job_flight',
        'job_passenger', 
        'job_booking',
        'job_baggage',
        'job_crew_assignment',
        'job_passenger_notification',
        'job_flight_incident',
        'job_flight_fuel',
        'job_maintenance_event'
    ]
    
    # Wait for database to be ready
    print("⏳ Waiting for database to be ready...")
    time.sleep(10)
    
    success_count = 0
    
    for proc in procedures:
        if test_procedure(proc):
            success_count += 1
        time.sleep(2)  # Wait between tests
    
    print("=" * 50)
    print(f"📈 Test Results: {success_count}/{len(procedures)} procedures successful")
    
    if success_count == len(procedures):
        print("🎉 All procedures are working correctly!")
    else:
        print("⚠️ Some procedures failed. Check logs for details.")

if __name__ == "__main__":
    main() 