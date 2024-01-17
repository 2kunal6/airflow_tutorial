from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from common.common_tasks import send_metrics
from util.load_config import load_config

import yaml


with open('config/application_config.yaml') as app_config_file:
    app_config =  yaml.safe_load(app_config_file)

config = load_config()

def load_data(**kwargs):
    # For non-prod environments do not get entire data to save cost.  Just get enough of data for testing.
    limit_query = ''
    if(Variable.get("environment") != 'prod'):
        limit_query = ' LIMIT 1000 '
    sample_query = f'INSERT INTO {kwargs["db_schema_name"]}.SOURCE_{kwargs["app"]}_{kwargs["table_type"]} ' \
                   f'SELECT * FROM {kwargs["db_schema_name"]}.DESTINATION_{kwargs["app"]}_{kwargs["table_type"]} ' \
                   f'WHERE data_date = "{kwargs["run_date"]}" ' \
                   f'{limit_query}'
    print(f'Running query: {sample_query}')

def get_data_load_operator(app, table_type):
    return PythonOperator(task_id=f'{app}_{table_type}',
                          op_kwargs={'app': app,
                                     'table_type': table_type,
                                     'db_schema_name': config['environment_properties']['db_schema_name'],
                                     # If we use execution_date then we might get the wrong date if Airflow server goes down for an entire day
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
