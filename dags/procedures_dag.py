from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta
import sys
import os

# Default arguments
default_args = {
    'owner': 'swen-airlines',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
}

# PostgreSQL connection ID
POSTGRES_CONN_ID = 'postgres_default'

# Prosedür listesi
PROCEDURES = [
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

# Her prosedür için ayrı DAG oluştur
for proc_name in PROCEDURES:
    dag_id = f'realtime_{proc_name}'
    
    dag = DAG(
        dag_id,
        default_args=default_args,
        description=f'Her 3 dakikada {proc_name} prosedürünü çalıştırır - Realtime ETL',
        schedule_interval=timedelta(minutes=3),
        start_date=datetime(2024, 1, 1),
        catchup=False,
        max_active_runs=1,
        tags=['realtime', 'procedures', 'etl', 'ft-to-tr']
    )
    
    # PostgreSQL procedure task
    run_procedure = PostgresOperator(
        task_id=f'run_{proc_name}',
        postgres_conn_id=POSTGRES_CONN_ID,
        sql=f"CALL {proc_name}('delta');",
        dag=dag,
        pool='default_pool'
    )
    
    # DAG'ı global scope'a ekle
    globals()[dag_id] = dag 