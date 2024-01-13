from airflow import DAG
from airflow.operators.python import PythonOperator

def get_task_details(**kwargs):
    print('\n\nkwargs-------------------------------------------------------------')
    for k, v in kwargs.items():
        print(k, v)

    print('\n\nkwargs["dag"]------------------------------------------------------')
    print(kwargs['dag'].dag_id)
    #print('{{ dag }}') This syntax is not supported in python callable

    print('\n\nkwargs["dag_run"]--------------------------------------------------')
    print(kwargs['dag_run'].execution_date)

    print('\n\nkwargs["ti"]-------------------------------------------------------')
    print(kwargs['ti'].state)

    print('-----------------------------------------------------------------------')


def get_task_details_template(execution_date_jinja):
    print('jinja template execution date: ' + str(execution_date_jinja))

with DAG(dag_id='a_accessing_parameters_dag'):
    PythonOperator(
        task_id="python_task",
        python_callable=get_task_details,
    )
    PythonOperator(
        task_id="python_kwargs_task",
        python_callable=get_task_details_template,
        op_args=['{{ dag_run.execution_date }}']
    )
