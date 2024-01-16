def num_failed_tasks_metric(dag_run):
    num_unsucessful_tasks = 0
    for task_instance in dag_run.get_task_instances():
        if(task_instance.state.lower() != 'success'):
            num_unsucessful_tasks += 1

    print(f'sending metric (for example to grafana): num_unsucessful_tasks = {num_unsucessful_tasks}')


def send_metrics(**kwargs):
    dag_run = kwargs['dag_run']
    num_failed_tasks_metric(dag_run)
