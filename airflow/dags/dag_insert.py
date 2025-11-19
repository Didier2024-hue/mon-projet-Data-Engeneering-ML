from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "didier",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="cde_insert_pipeline",
    default_args=default_args,
    description="Insertion Wiki / PostgreSQL / MongoDB",
    schedule_interval=None,      # Lancement manuel (tests)
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["cde", "insert", "trustpilot"],
) as dag:

    run_all_insert = BashOperator(
        task_id="run_all_insert_sh",
        # 🔥 IMPORTANT : le fichier est à la racine de /opt/airflow/cde
        bash_command="bash -c '/opt/airflow/cde/run_all_insert.sh'",
    )
