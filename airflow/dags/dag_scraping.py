from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from airflow.utils.dates import days_ago

DAG_ID = "cde_scraping_pipeline"

default_args = {
    "owner": "didier",
    "depends_on_past": False,
    "retries": 0,
}

with DAG(
    dag_id=DAG_ID,
    description="Pipeline de scraping Trustpilot + Wikipedia pour le projet CDE",
    start_date=days_ago(1),
    schedule_interval=None,   # exécution manuelle uniquement
    catchup=False,
    tags=["scraping", "trustpilot", "wikipedia", "cde"],
) as dag:

    # -------------------------
    # SECTION 1 — Contexte
    # -------------------------
    log_start = BashOperator(
        task_id="afficher_contexte",
        bash_command='echo "=== Début du scraping CDE ($(date)) ==="',
        do_xcom_push=False,
    )

    # -------------------------
    # SECTION 2 — SCRAPING
    # -------------------------
    with TaskGroup("scraping") as scraping_group:

        run_scraping = BashOperator(
            task_id="run_all_scraping",
            bash_command="bash -c '/opt/airflow/cde/run_all_scraping.sh'",
            do_xcom_push=False,
        )

    # -------------------------
    # SECTION 3 — Fin
    # -------------------------
    log_end = BashOperator(
        task_id="fin_pipeline",
        bash_command='echo "=== Fin du scraping CDE ($(date)) ==="',
        do_xcom_push=False,
    )

    # Dépendances
    log_start >> scraping_group >> log_end
