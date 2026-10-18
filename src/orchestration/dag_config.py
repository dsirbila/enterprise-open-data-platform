"""lecture 18: Dynamic DAG-ების კონფიგურაცია — ერთი config სია, საიდანაც რამდენიმე დამოუკიდებელი DAG გენერირდება loop-ით."""
from dataclasses import dataclass

@dataclass(frozen=True)
class SourceDagConfig:
    source_name: str
    dag_id: str
    schedule: str
    task_function_name: str  # ingestion_tasks.py-ში function-ის სახელი

SOURCE_CONFIGS = [
    SourceDagConfig(
        source_name="weather",
        dag_id="ingest_weather",
        schedule="0 6 * * *",
        task_function_name="fetch_weather_task",
    ),
    SourceDagConfig(
        source_name="currency",
        dag_id="ingest_currency",
        schedule="0 7 * * *",  # NBG-ის კურსი დილით ჩნდება — 1 საათით გვიან
        task_function_name="fetch_currency_task",
    ),
    SourceDagConfig(
        source_name="seismic",
        dag_id="ingest_seismic",
        schedule="*/30 * * * *",  # ყოველ 30 წუთში — მიწისძვრები დროში არაპროგნოზირებადია
        task_function_name="fetch_seismic_task_daily",
    ),
]

def generate_dag_ids() -> list:
    """testable helper — რეალურ DAG loop-ს რომ არ სჭირდებოდეს Airflow ტესტვისთვის."""
    return [cfg.dag_id for cfg in SOURCE_CONFIGS]

def get_config_by_dag_id(dag_id: str) -> SourceDagConfig:
    for cfg in SOURCE_CONFIGS:
        if cfg.dag_id == dag_id:
            return cfg
    raise ValueError(f"უცნობი dag_id: {dag_id}")
