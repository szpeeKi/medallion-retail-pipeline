from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from airflow.sdk import dag, task

SP_TZ = ZoneInfo('America/Sao_Paulo')


@dag(
    # A captura da Lambda roda as 21h com ate 3 retentativas: 21h30 da folga para ela terminar.
    schedule='30 21 * * *',
    start_date=datetime(2026, 8, 1, tzinfo=SP_TZ),
    catchup=False,
    max_active_runs=1,
    default_args={'retries': 2, 'retry_delay': timedelta(minutes=10)},
    tags=['medallion'],
)
def medallion_retail():
    """Bronze -> Silver -> Gold, uma vez por dia, depois da captura das 21h."""

    @task
    def load_bronze(logical_date=None, dag_run=None):
        from src.load import load_bronze as bronze

        # O Airflow guarda as datas em UTC, e 21h30 em Sao Paulo ja e o dia seguinte em UTC.
        # Por isso a conversao para o fuso de Sao Paulo antes de pegar o dia.
        # Num disparo manual pela interface pode nao existir logical_date: ai vale o run_after.
        reference = logical_date or dag_run.run_after
        bronze.run(reference.astimezone(SP_TZ).date())

    @task
    def transform_silver():
        from src.transform import transform_silver as silver

        silver.run()

    @task
    def build_gold():
        from src.transform import build_gold as gold

        gold.run()

    load_bronze() >> transform_silver() >> build_gold()


medallion_retail()
