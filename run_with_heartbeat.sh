#!/bin/bash

CMD="$1"
LOGFILE="$2"

# Lancer la commande en arrière-plan
bash -c "$CMD" >> "$LOGFILE" 2>&1 &
PID=$!

# Heartbeat
while kill -0 $PID 2>/dev/null; do
    echo "[AIRFLOW] running..."
    sleep 5
done

wait $PID
echo "[AIRFLOW] finished"
