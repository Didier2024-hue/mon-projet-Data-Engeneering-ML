from datetime import timedelta
from airflow import DAG
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.ssh.hooks.ssh import SSHHook
from airflow.utils.dates import days_ago

# ========================
# CONFIG
# ========================
BASE = "/home/datascientest/cde"
VENV = f"{BASE}/cde_env/bin/activate"

ssh_hook = SSHHook(
    ssh_conn_id="ssh_datascientest",
    keepalive_interval=30
)

default_args = {
    "owner": "datascientest",
    "depends_on_past": False,
    "retries": 0
}

# ========================
# Scripts ML EXACTS
# (ordre imposé)
# ========================
ML_SCRIPTS = [
    ("ml_snapshot_data",       "scripts/preprocess/snapshot_data.py"),
    ("ml_clean_data",          "scripts/preprocess/clean_data.py"),
    ("ml_preprocess_avis",     "scripts/preprocess/preprocess_clean_avis.py"),
    ("ml_sentiment",           "scripts/preprocess/sentiment_analysis.py"),
    ("ml_train_models",        "scripts/models/train_dual_models.py"),
]


# ==========================================================
# HEARTBEAT WRAPPER — version PRO sans parenthèses
# ==========================================================
def heartbeat_wrapper(script_cmd, logfile):
    return (
        "{ "
        f"{script_cmd} > {logfile} 2>&1 & "
        "PID=$! ; "
        "while kill -0 $PID 2>/dev/null; do "
        "  echo \"[AIRFLOW] still running...\" ; "
        f"  tail -n 10 {logfile} ; "
        "  sleep 5 ; "
        "done ; "
        "wait $PID ; "
        "echo \"[AIRFLOW] step finished\" ; "
        "}"
    )


# ========================
# DAG
# ========================
with DAG(
    dag_id="cde_master_pipeline",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    max_active_runs=1,
    tags=["pro", "final", "stable"],
):

    # ======================================================
    # 1) SCRAPING
    # ======================================================
    scraping = SSHOperator(
        task_id="scraping",
        ssh_hook=ssh_hook,
        command=(
            f"bash -lc '"
            f"source {VENV} ; cd {BASE} ; "
            f"{heartbeat_wrapper(f'bash run_all_scraping.sh', f'{BASE}/logs/scraping.log')}'"
        ),
        get_pty=False,
        execution_timeout=timedelta(hours=4),
    )

    # ======================================================
    # 2) INSERTION
    # ======================================================
    insertion = SSHOperator(
        task_id="insertion",
        ssh_hook=ssh_hook,
        command=(
            f"bash -lc '"
            f"source {VENV} ; cd {BASE} ; "
            f"{heartbeat_wrapper(f'bash run_all_insert.sh', f'{BASE}/logs/insertion.log')}'"
        ),
        get_pty=False,
        execution_timeout=timedelta(hours=4),
    )

    # Orchestration
    scraping >> insertion

    # ======================================================
    # 3) MACHINE LEARNING — 5 scripts découpés
    # ======================================================
    previous = insertion

    for task_name, script_path in ML_SCRIPTS:
        ml_task = SSHOperator(
            task_id=task_name,
            ssh_hook=ssh_hook,
            command=(
                f"bash -lc '"
                f"source {VENV} ; cd {BASE} ; "
                f"{heartbeat_wrapper(f'python3 {BASE}/{script_path}', f'{BASE}/logs/{task_name}.log')}'"
            ),
            get_pty=False,
            execution_timeout=timedelta(hours=3),
        )

        previous >> ml_task
        previous = ml_task
