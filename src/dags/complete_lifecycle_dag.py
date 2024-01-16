from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from common.common_tasks import send_metrics

import yaml


with open('config/application_config.yaml') as app_config_file:
    app_config =  yaml.safe_load(app_config_file)


for dag_type in app_config['salesforce']:
    with DAG(dag_id=dag_type) as dag:
        send_metrics_task = PythonOperator(task_id = f'{dag_type}_metric_task',
                                           python_callable = send_metrics,
                                           trigger_rule = 'all_done',
                                           dag = dag)
        for app in app_config['salesforce'][dag_type]:
            for table_type in app_config['salesforce'][dag_type][app]:
                EmptyOperator(task_id=f'{app}_{table_type}') >> send_metrics_task
