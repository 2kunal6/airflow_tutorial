from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

def python_callable_function():
    print("Executing callee task")

default_args = {
    'start_date': datetime(2024, 1, 10),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'a_external_sensor_callee_dag',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
):
    PythonOperator(
        task_id='a_external_sensor_callee_task',
        python_callable=python_callable_function,
        provide_context=True,
    )
