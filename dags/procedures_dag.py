from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

# Default arguments
default_args = {
    'owner': 'swen-airlines',
    'depends_on_past': False,
    'start_date': datetime.now() - timedelta(minutes=5),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
}

# Procedure list for Swen Airlines DWH
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

# Create a separate DAG for each procedure with 3-minute interval
for procedure_name in PROCEDURES:
    dag_id = f"{procedure_name}_dag"
    
    dag = DAG(
        dag_id=dag_id,
        default_args=default_args,
        description=f'Run {procedure_name} procedure every 3 minutes in delta mode',
        schedule_interval=timedelta(minutes=3),
        start_date=datetime.now() - timedelta(minutes=5),
        catchup=False,
        max_active_runs=1,
        tags=['swen_airlines', 'procedures', 'delta']
    )
    
    # Create task for this procedure
    task = PostgresOperator(
        task_id=f'run_{procedure_name}',
        postgres_conn_id='postgres_swen_dwh',  # Updated connection ID
        sql=f"CALL {procedure_name}('delta');",
        dag=dag
    )
    
    # Add to globals so Airflow can discover it
    globals()[dag_id] = dag 