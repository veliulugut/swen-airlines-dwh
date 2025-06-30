#!/usr/bin/env python3
"""
Swen Airlines DWH System Status Checker
Bu script sistem durumunu kontrol eder.
"""
import subprocess
import time
import psycopg2

def check_docker_services():
    """Docker servislerinin durumunu kontrol eder"""
    print("🐳 Docker Services Status:")
    try:
        result = subprocess.run(['docker', 'ps', '--format', 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'], 
                              capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"❌ Docker kontrol hatası: {e}")

def check_database():
    """PostgreSQL bağlantısını ve tablo durumunu kontrol eder"""
    print("\n🗄️ Database Status:")
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="swen_dwh",
            user="admin",
            password="admin"
        )
        cursor = conn.cursor()
        
        # FT tabloları row count
        ft_tables = ['ft_flight', 'ft_passenger', 'ft_booking', 'ft_baggage', 
                    'ft_crew_assignment', 'ft_passenger_notification', 'ft_flight_incident',
                    'ft_flight_fuel', 'ft_maintenance_event']
        
        print("📊 FT Tables (Raw Data from Kafka):")
        for table in ft_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   {table}: {count} rows")
            
        # TR tabloları row count  
        tr_tables = ['tr_flight', 'tr_passenger', 'tr_booking', 'tr_baggage',
                    'tr_crew_assignment', 'tr_passenger_notification', 'tr_flight_incident',
                    'tr_flight_fuel', 'tr_maintenance_event']
        
        print("\n📈 TR Tables (Report Data for Dashboard):")
        for table in tr_tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   {table}: {count} rows")
            except:
                print(f"   {table}: Not created yet")
                
        conn.close()
        print("✅ Database connection successful")
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

def check_kafka_topics():
    """Kafka topics durumunu kontrol eder"""
    print("\n📡 Kafka Status:")
    try:
        # Docker container içindeki kafka-topics komutunu çalıştır
        result = subprocess.run([
            'docker', 'exec', 'swen-airlines-dwh-kafka-1', 
            'kafka-topics', '--bootstrap-server', 'localhost:9092', '--list'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            topics = result.stdout.strip().split('\n')
            print(f"📝 Active Topics ({len(topics)}):")
            for topic in topics:
                if topic.strip():
                    print(f"   • {topic}")
            print("✅ Kafka topics accessible")
        else:
            print("❌ Kafka topics not accessible yet")
            
    except Exception as e:
        print(f"❌ Kafka check failed: {e}")

def check_airflow_dags():
    """Airflow DAG durumunu kontrol eder"""
    print("\n⏰ Airflow DAGs Status:")
    try:
        result = subprocess.run([
            'docker', 'exec', 'swen-airlines-dwh-airflow-webserver-1',
            'airflow', 'dags', 'list'
        ], capture_output=True, text=True)
        
        if "ft_kafka_to_postgres" in result.stdout and "procedures_dag" in result.stdout:
            print("✅ Both DAGs are available")
            print("   • ft_kafka_to_postgres (Kafka → PostgreSQL every 5 min)")
            print("   • procedures_dag (Data transformation every 3 min)")
        else:
            print("❌ DAGs not ready yet")
            
    except Exception as e:
        print(f"❌ Airflow check failed: {e}")

def main():
    print("=" * 60)
    print("🛫 SWEN AIRLINES DWH - SYSTEM STATUS CHECK")
    print("=" * 60)
    
    check_docker_services()
    time.sleep(1)
    
    check_database()
    time.sleep(1)
    
    check_kafka_topics() 
    time.sleep(1)
    
    check_airflow_dags()
    
    print("\n" + "=" * 60)
    print("🌐 Access Points:")
    print("   📊 Dashboard: http://localhost:8501")
    print("   ⚙️ Airflow UI: http://localhost:8080 (admin/admin)")
    print("   🗄️ Database: localhost:5432 (admin/admin)")
    print("=" * 60)

if __name__ == "__main__":
    main() 