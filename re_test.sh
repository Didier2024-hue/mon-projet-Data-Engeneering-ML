docker exec -i fastapi-cde python - <<'PY'
import os, glob, joblib, warnings, sys
from sklearn.exceptions import InconsistentVersionWarning
from sklearn import __version__ as runtime

roots = [
    os.getenv("DATA_MODEL") or "/app/data/model",
    "/app/data/model",
    "/app",
    "/home/datascientest/cde/mlruns",  # au cas où MLflow soit monté tel quel
    "/app/mlruns",
]

seen = set()
cands = []
for root in roots:
    if not root or not os.path.isdir(root): 
        continue
    for ext in ("*.pkl", "*.joblib", "*.sav", "*.pkl.gz"):
        for f in glob.glob(os.path.join(root, "**", ext), recursive=True):
            if os.path.isfile(f):
                cands.append(os.path.realpath(f))

cands = sorted(set(cands))
print("Runtime scikit-learn:", runtime)
if not cands:
    print("Aucun artefact trouvé sous:", roots)
    sys.exit(0)

bad = 0
for f in cands:
    try:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always", InconsistentVersionWarning)
            obj = joblib.load(f)
        saved = getattr(obj, "_sklearn_version", None)
        print(f"\n• {f}\n   saved={saved}  type={type(obj).__name__}")
        if hasattr(obj, "steps"):
            for name, step in getattr(obj, "steps", []):
                sv = getattr(step, "_sklearn_version", None)
                print(f"     - step '{name}': {type(step).__name__} saved={sv}")
        for warn in w:
            if issubclass(warn.category, InconsistentVersionWarning):
                bad += 1
                print("   !! InconsistentVersionWarning:", str(warn.message).splitlines()[0])
    except Exception as e:
        print(f"\n• {f}\n   ERROR: {e}")

print(f"\nTotal artefacts scannés: {len(cands)} | avec warning de version: {bad}")
PY

