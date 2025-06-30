#!/usr/bin/env python3
"""
DAG Activation Script for Swen Airlines DWH
This script automatically unpauses/activates all DAGs
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
            result = subprocess.run(['airflow', 'dags', 'list'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ Airflow is ready!")
                return True
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        retry_count += 1
        print(f"⏳ Attempt {retry_count}/{max_retries} - Airflow not ready yet...")
        time.sleep(2)
    
    print("❌ Failed to connect to Airflow after 30 attempts")
    return False

def activate_all_dags():
    """Activate all DAGs in Airflow"""
    if not wait_for_airflow():
        sys.exit(1)
    
    try:
        # Get list of all DAGs
        print("📋 Getting list of DAGs...")
        result = subprocess.run(['airflow', 'dags', 'list'], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Failed to get DAG list: {result.stderr}")
            return
        
        # Extract DAG IDs from output
        lines = result.stdout.strip().split('\n')
        dag_ids = []
        
        # Look for lines that contain dag IDs (skip header and separator lines)
        for line in lines:
            if '|' in line and not line.startswith('dag_id') and not line.startswith('---'):
                parts = line.split('|')
                if len(parts) >= 2:
                    dag_id = parts[0].strip()
                    if dag_id and not dag_id.startswith('-'):
                        dag_ids.append(dag_id)
        
        if not dag_ids:
            print("ℹ️ No DAGs found or DAGs already processed")
            return
        
        print(f"🎯 Found {len(dag_ids)} DAGs to activate")
        
        # Activate each DAG
        for dag_id in dag_ids:
            try:
                print(f"▶️ Activating DAG: {dag_id}")
                result = subprocess.run(['airflow', 'dags', 'unpause', dag_id], 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"✅ DAG {dag_id} activated successfully")
                else:
                    print(f"⚠️ Warning: Failed to activate {dag_id}: {result.stderr}")
                    
            except Exception as e:
                print(f"⚠️ Warning: Error activating {dag_id}: {e}")
        
        print("✅ DAG activation completed!")
        
        # Show final status
        print("\n📊 DAG Status Summary:")
        result = subprocess.run(['airflow', 'dags', 'list'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'realtime_job_' in line or 'ft_kafka_to_postgres' in line:
                    print(f"   {line}")
        
    except Exception as e:
        print(f"❌ Error activating DAGs: {e}")
        sys.exit(1)

if __name__ == "__main__":
    activate_all_dags() 