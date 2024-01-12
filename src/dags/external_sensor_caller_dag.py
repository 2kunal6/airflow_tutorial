# TODO: Fix this
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from datetime import timedelta

import pendulum

def task_two():
    print("Executing task_two")

with DAG('a_external_sensor_caller_dag'):
    sensor_task = ExternalTaskSensor(
        task_id='external_sensor_caller_task',
        external_dag_id='a_external_sensor_callee_dag',
        external_task_id='a_external_sensor_callee_task',
        timeout=600,
        execution_delta=timedelta(minutes=1),
        #schedule_interval=timedelta(seconds=5),
        start_date=pendulum.datetime(2024, 1, 6, tz="UTC")
    )

    task_two = PythonOperator(
        task_id='external_sensor_dependent_task',
        python_callable=task_two
    )

    sensor_task >> task_two
