from airflow import DAG
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.ssh.hooks.ssh import SSHHook
from airflow.utils.dates import days_ago

default_args = {
    "owner": "datascientest",
    "depends_on_past": False,
}

# Connexion SSH Airflow → host
ssh_hook = SSHHook(
    ssh_conn_id="ssh_datascientest",
    keepalive_interval=30   # Empêche l'inactivité SSH
)

with DAG(
    dag_id="cde_ml_pipeline",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=["cde","ml", "ssh", "nohup"],
) as dag:

    # On exécute le script ML en arrière-plan via nohup
    run_ml_pipeline = SSHOperator(
        task_id="cde_ml_pipeline",
        ssh_hook=ssh_hook,
        get_pty=False,   # Important pour éviter les coupures Paramiko
        command=(
            "bash -lc '"
            "nohup bash /home/datascientest/cde/run_all_ml.sh "
            "> /home/datascientest/cde/logs/run_all_ml_airflow_nohup.out 2>&1 &'"
        ),
    )

