import sys

from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.append('../')
from util.load_config import load_config

def python_callable():
    config = load_config()
    print(config)


with DAG(dag_id='a_admin_variable_access_dag',
):
    PythonOperator(
        task_id="python_task",
        python_callable=python_callable,
    )
