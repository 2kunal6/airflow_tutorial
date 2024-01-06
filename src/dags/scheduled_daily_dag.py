from airflow import DAG
from airflow.operators.empty import EmptyOperator
import pendulum

with DAG(dag_id='a_scheduled_daily_dag',
    schedule="10 10 * * *", # accepts a cron expression
    start_date=pendulum.datetime(2024, 1, 6, tz="UTC"),
    catchup=False
):
    EmptyOperator(task_id="an_empty_task")
