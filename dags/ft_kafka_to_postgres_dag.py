from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Consumer modülünü import edebilmek için path ekle
sys.path.append('/opt/airflow')

def run_kafka_consumer():
    """Kafka'dan PostgreSQL'e veri aktaran task"""
    try:
        from consumers.consumer import run_kafka_to_postgres_batch
        print("[Airflow Task] Kafka consumer task başlatıldı")
        run_kafka_to_postgres_batch()
        print("[Airflow Task] Kafka consumer task tamamlandı")
    except Exception as e:
        print(f"[Airflow Task][ERROR] Consumer task hatası: {e}")
        raise

default_args = {
    'owner': 'swen-airlines',
    'depends_on_past': False,
    'start_date': datetime.now() - timedelta(minutes=10),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'ft_kafka_to_postgres',
    default_args=default_args,
    description='Kafka FT verilerini her 5 dakikada bir PostgreSQL FT tablolarına yükler',
    schedule_interval=timedelta(minutes=5),
    start_date=datetime.now() - timedelta(minutes=10),
    catchup=False,
    max_active_runs=1,
    tags=['kafka', 'postgres', 'etl', 'fact-tables']
)

# Kafka'dan PostgreSQL'e veri aktarım task'i
kafka_to_postgres_task = PythonOperator(
    task_id='kafka_to_postgres_transfer',
    python_callable=run_kafka_consumer,
    dag=dag,
    pool='default_pool',
    max_active_tis_per_dag=1
) 