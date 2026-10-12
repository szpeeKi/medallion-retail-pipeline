import logging

from airflow.sdk import dag, task

logger = logging.getLogger(__name__)


@dag(schedule=None, catchup=False, tags=['teste'])
def hello_airflow():
    """DAG de teste: uma task que so escreve no log, para provar que o Airflow esta de pe."""

    @task
    def say_hello():
        logger.info('Hello from Airflow!')

    say_hello()


hello_airflow()
