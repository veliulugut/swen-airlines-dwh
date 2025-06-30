#!/usr/bin/env python3
"""
Initial Bulk Procedures Runner for Swen Airlines DWH
This script runs all job procedures in 'bulk' mode for initial data load
"""

import psycopg2
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

def check_procedures_exist():
    """Check if stored procedures exist"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT routine_name 
            FROM information_schema.routines 
            WHERE routine_type = 'PROCEDURE' 
            AND routine_name LIKE 'job_%'
            ORDER BY routine_name
        """)
        
        procedures = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        return procedures
        
    except Exception as e:
        print(f"❌ Error checking procedures: {e}")
        return []

def run_initial_procedures():
    """Run initial bulk load procedures"""
    if not wait_for_db():
        sys.exit(1)
    
    try:
        # Check if procedures exist
        procedures = check_procedures_exist()
        
        if not procedures:
            print("⚠️ No stored procedures found. They should be auto-loaded by PostgreSQL init.")
            print("ℹ️ Continuing anyway - procedures will be loaded by Airflow later.")
            return
        
        print(f"📋 Found {len(procedures)} procedures: {', '.join(procedures)}")
        
        # List of procedures to run in order
        procedure_order = [
            'job_flight',
            'job_passenger', 
            'job_booking',
            'job_crew_assignment',
            'job_flight_fuel',
            'job_maintenance_event',
            'job_baggage',
            'job_flight_incident',
            'job_passenger_notification'
        ]
        
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("🚀 Starting initial bulk procedures...")
        
        for procedure_name in procedure_order:
            if procedure_name in procedures:
                try:
                    print(f"▶️ Running {procedure_name}('full')...")
                    cursor.execute(f"CALL {procedure_name}('full')")
                    conn.commit()
                    print(f"✅ {procedure_name} completed successfully")
                except Exception as e:
                    print(f"⚠️ Warning: {procedure_name} failed: {e}")
                    # Continue with other procedures even if one fails
                    conn.rollback()
            else:
                print(f"⚠️ Procedure {procedure_name} not found, skipping...")
        
        cursor.close()
        conn.close()
        
        print("✅ Initial bulk procedures completed!")
        
        # Log the results
        print("\n📊 Checking table counts after bulk load:")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        tables = ['tr_flight', 'tr_passenger', 'tr_booking', 'tr_crew_assignment', 
                 'tr_flight_fuel', 'tr_maintenance_event', 'tr_baggage', 
                 'tr_flight_incident', 'tr_passenger_notification']
        
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   📋 {table}: {count:,} records")
            except Exception as e:
                print(f"   ❌ {table}: Error - {e}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error running initial procedures: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_initial_procedures() 