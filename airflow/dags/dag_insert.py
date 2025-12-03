from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.ssh.operators.ssh import SSHOperator

default_args = {
    "owner": "datascientest",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="cde_insert_pipeline",
    default_args=default_args,
    description="Insertion Wiki / PostgreSQL / MongoDB",
    schedule_interval=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["cde", "insert", "trustpilot"],
) as dag:

    run_all_insert = SSHOperator(
        task_id="run_all_insert_sh",
        ssh_conn_id="ssh_datascientest",
        command="bash /home/datascientest/cde/run_all_insert.sh",
        cmd_timeout=600,   # ⬅️ 10 minutes
    )

    # Désactivation templating
    run_all_insert.template_fields = ()
