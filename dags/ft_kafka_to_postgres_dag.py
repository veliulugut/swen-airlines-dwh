from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess

def run_consumer():
    # Consumer scriptini çalıştır (her 5 dakikada bir batch yükleme için)
    subprocess.run(["python", "consumers/consumer.py"])  # Gerekirse tam path verilebilir

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

dag = DAG(
    'ft_kafka_to_postgres',
    default_args=default_args,
    description='Kafka FT verilerini her 5 dakikada bir Postgres FT tablolarına yükler',
    schedule_interval=timedelta(minutes=5),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
)

consume_task = PythonOperator(
    task_id='consume_kafka_to_postgres',
    python_callable=run_consumer,
    dag=dag,
) 