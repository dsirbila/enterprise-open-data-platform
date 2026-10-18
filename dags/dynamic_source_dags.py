"""lecture 18: Dynamic DAG generation — ერთი config სია, სამი დამოუკიდებელი DAG."""
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from src.orchestration import ingestion_tasks
from src.orchestration.dag_config import SOURCE_CONFIGS

default_args = {
    "owner": "data-engineering",
    "retries": 3,
    "retry_delay": timedelta(seconds=30),
    "retry_exponential_backoff": True,
    "max_retry_delay": timedelta(minutes=5),
}

def make_dag(config):
    @dag(
        dag_id=config.dag_id,
        schedule=config.schedule,
        start_date=datetime(2026, 8, 1),
        catchup=False,
        default_args=default_args,
        tags=["ingestion", config.source_name, "dynamic"],
    )
    def _dag():
        @task
        def fetch():
            task_fn = getattr(ingestion_tasks, config.task_function_name)
            return task_fn()

        fetch()

    return _dag()

# ერთი loop-ით სამი დამოუკიდებელი DAG — Airflow-ს globals()-ში უნდა "დაინახოს" თითოეული
for cfg in SOURCE_CONFIGS:
    globals()[cfg.dag_id] = make_dag(cfg)
