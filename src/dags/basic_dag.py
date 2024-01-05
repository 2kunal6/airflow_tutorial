from airflow import DAG
from airflow.operators.empty import EmptyOperator

with DAG(dag_id='a_basic_dag'):
    EmptyOperator(task_id="an_empty_task")
