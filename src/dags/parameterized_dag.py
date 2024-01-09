from airflow import DAG
from airflow.operators.python import PythonOperator


# Accessing params directly
def python_callable(params):
    print(params['param_name'])

# Accessing via context
def python_callable_context(**context):
    print(context['params']['param_name'])

# Accessing via jinja templating
def python_callable_jinja(param_val):
    print('{{ params.param_name }}')
    print(param_val)

def python_callable_kwargs(**kwargs):
    print(kwargs['params']['param_name'])


with DAG(dag_id='a_parameterized_dag',
    params={
        "param_name": "dag value"
     },
):
    PythonOperator(
        task_id="python_task",
        python_callable=python_callable,
    )

    PythonOperator(
        task_id="python_task_context",
        params={
            "param_name": "task value"
        },
        python_callable=python_callable_context,
    )

    PythonOperator(
        task_id="python_task_jinja",
        op_args=['{{ params.param_name }}'],
        python_callable=python_callable_jinja,
    )

    PythonOperator(
        task_id="python_task_kwargs",
        python_callable=python_callable_kwargs,
    )
