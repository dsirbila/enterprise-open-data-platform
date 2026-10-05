"""lecture 17: პირველი DAG — ყოველდღიური ingestion სამივე წყაროსთვის."""
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from src.orchestration.ingestion_tasks import (
    fetch_currency_task,
    fetch_seismic_task,
    fetch_weather_task,
    summarize_run,
)

default_args = {
    "owner": "data-engineering",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

@dag(
    dag_id="daily_ingestion",
    schedule="0 6 * * *",
    start_date=datetime(2026, 8, 1),
    catchup=False,
    default_args=default_args,
    tags=["ingestion", "weather", "currency", "seismic"],
)
def daily_ingestion_dag():
    @task
    def fetch_weather() -> dict:
        return fetch_weather_task()

    @task
    def fetch_currency() -> dict:
        return fetch_currency_task()

    @task
    def fetch_seismic() -> dict:
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        return fetch_seismic_task(start_date, end_date)

    @task
    def summarize(weather_result: dict, currency_result: dict, seismic_result: dict) -> str:
        return summarize_run(weather_result, currency_result, seismic_result)

    weather_result = fetch_weather()
    currency_result = fetch_currency()
    seismic_result = fetch_seismic()
    summarize(weather_result, currency_result, seismic_result)

daily_ingestion_dag()
