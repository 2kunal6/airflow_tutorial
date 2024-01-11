import yaml

from airflow.models import Variable


def load_config():
    env = 'dev'
    if(Variable.get("environment") == 'prod'):
        env = 'prod'
    with open('config/config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config[env]
