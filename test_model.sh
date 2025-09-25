#!/usr/bin/env bash
set -euo pipefail

CONTAINER=fastapi-cde
docker exec -i "$CONTAINER" python - <<'PY'
import os, glob, joblib
from sklearn import __version__ as runtime

root = "/app/data/model"
print("Runtime scikit-learn:", runtime)
found = False

for f in glob.glob(os.path.join(root, "**", "*"), recursive=True):
    if not os.path.isfile(f) or not f.endswith((".pkl", ".joblib")):
        continue
    found = True
    try:
        obj = joblib.load(f)
        saved = getattr(obj, "_sklearn_version", None)
        print(f"• {f}\n   saved={saved}  type={type(obj).__name__}")
        if hasattr(obj, "steps"):
            for name, step in obj.steps:
                print(f"     - step '{name}': {type(step).__name__} saved={getattr(step, '_sklearn_version', None)}")
    except Exception as e:
        print(f"• {f}\n   ERROR: {e}")

if not found:
    print("No .pkl/.joblib files found under", root)
PY
