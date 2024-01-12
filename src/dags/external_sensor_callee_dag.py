from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import timedelta

import pendulum

def task_one():
    print("Executing task_one")

with DAG('a_external_sensor_callee_dag',
         schedule_interval=timedelta(hours=24),
         start_date=pendulum.datetime(2024, 1, 12, tz="UTC")):
    PythonOperator(
        task_id='a_external_sensor_callee_task',
        python_callable=task_one
    )
