from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from common.common_tasks import send_metrics
from util.load_config import load_config

import yaml


with open('config/application_config.yaml') as app_config_file:
    app_config =  yaml.safe_load(app_config_file)

config = load_config()

def load_data(**kwargs):
    print(f'Loading data for following args:\n'
          f'app: {kwargs["app"]}\n'
          f'table_type: {kwargs["table_type"]}\n'
          f'db_schema_name: {kwargs["db_schema_name"]}\n'
          f'run_date: {kwargs["run_date"]}\n')


def get_data_load_operator(app, table_type):
    return PythonOperator(task_id=f'{app}_{table_type}',
                          op_kwargs={'app': app,
                                     'table_type': table_type,
                                     'db_schema_name': config['environment_properties']['db_schema_name'],
                                     'run_date': '{{ data_interval_end }}'
                                     },
                          python_callable=load_data)


for dag_type in app_config['salesforce']:
    with DAG(dag_id=dag_type) as dag:
        send_metrics_task = PythonOperator(task_id = f'{dag_type}_metric_task',
                                           python_callable = send_metrics,
                                           trigger_rule = 'all_done',
                                           dag = dag)
        for app in app_config['salesforce'][dag_type]:
            for table_type in app_config['salesforce'][dag_type][app]:

                data_load_task = get_data_load_operator(app, table_type)

                data_load_task >> send_metrics_task
