#!/usr/bin/env python3
"""
Airflow Connection Setup for Swen Airlines DWH
This script sets up PostgreSQL connection for DAGs to access swen_dwh database
"""

import subprocess
import time
import sys

def wait_for_airflow():
    """Wait for Airflow to be ready"""
    print("🔄 Waiting for Airflow to be ready...")
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            result = subprocess.run(['airflow', 'connections', 'list'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ Airflow is ready!")
                return True
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        retry_count += 1
        print(f"⏳ Attempt {retry_count}/{max_retries}: Waiting for Airflow...")
        time.sleep(5)
    
    print("❌ Airflow failed to become ready")
    return False

def setup_connections():
    """Set up PostgreSQL connection for Swen DWH"""
    if not wait_for_airflow():
        return False
    
    try:
        print("🔗 Setting up PostgreSQL connection for Swen DWH...")
        
        # Remove existing connection if exists
        subprocess.run(['airflow', 'connections', 'delete', 'postgres_swen_dwh'], 
                      capture_output=True)
        
        # Create new connection to swen_dwh database
        result = subprocess.run([
            'airflow', 'connections', 'add', 'postgres_swen_dwh',
            '--conn-type', 'postgres',
            '--conn-host', 'postgres',
            '--conn-port', '5432',
            '--conn-login', 'admin',
            '--conn-password', 'admin',
            '--conn-schema', 'swen_dwh'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ PostgreSQL connection (postgres_swen_dwh) created successfully!")
            
            # Verify connection
            verify_result = subprocess.run([
                'airflow', 'connections', 'get', 'postgres_swen_dwh'
            ], capture_output=True, text=True)
            
            if verify_result.returncode == 0:
                print("✅ Connection verified successfully!")
                return True
            else:
                print(f"⚠️ Connection verification failed: {verify_result.stderr}")
                return False
        else:
            print(f"❌ Failed to create connection: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error setting up connections: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Airflow connection setup...")
    
    if setup_connections():
        print("✅ Airflow connection setup completed successfully!")
        sys.exit(0)
    else:
        print("❌ Airflow connection setup failed!")
        sys.exit(1) 