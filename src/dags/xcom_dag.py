from airflow import DAG
from airflow.operators.python import PythonOperator


def python_callable_push(**kwargs):
    kwargs['ti'].xcom_push(key='example_key', value='example_xcom_value')

def python_callable_pull(**kwargs):
    print(kwargs['ti'].xcom_pull(task_ids='python_push_task', key='example_key'))


with DAG(dag_id='a_xcom_dag'):
    python_push_task = PythonOperator(
        task_id="python_push_task",
        python_callable=python_callable_push,
    )

    python_pull_task = PythonOperator(
        task_id="python_pull_task",
        python_callable=python_callable_pull,
    )

    # This is the task dependency
    python_push_task >> python_pull_task
