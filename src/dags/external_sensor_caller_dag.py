from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor

def python_callable_function():
    print("Executing task_two")


default_args = {
    'start_date': datetime(2024, 1, 10),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'a_external_sensor_caller_dag',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
):
    sensor_task = ExternalTaskSensor(
        task_id='external_sensor',
        external_dag_id='a_external_sensor_callee_dag',
        external_task_id='a_external_sensor_callee_task',
        mode='poke',
        poke_interval=60,
        timeout=600,
        retries=10,
    )

    task_two = PythonOperator(
        task_id='task_two',
        python_callable=python_callable_function,
        provide_context=True,
    )

    sensor_task >> task_two
