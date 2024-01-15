from airflow import DAG
from airflow.operators.empty import EmptyOperator

import yaml


with open('config/application_config.yaml') as app_config_file:
    app_config =  yaml.safe_load(app_config_file)


for dag_type in app_config['salesforce']:
    with DAG(dag_id=dag_type):
        for app in app_config['salesforce'][dag_type]:
            EmptyOperator(task_id=app)
