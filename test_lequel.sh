docker exec -i fastapi-cde python - <<'PY'
import os, glob, joblib, warnings
from sklearn.exceptions import InconsistentVersionWarning
from sklearn import __version__ as runtime

root = "/app/data/model"
print("Runtime scikit-learn:", runtime)
files = [f for f in glob.glob(os.path.join(root, "**", "*"), recursive=True)
         if os.path.isfile(f) and f.endswith((".pkl", ".joblib"))]

if not files:
    print("Aucun artefact .pkl/.joblib trouvé sous", root)

for f in files:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", InconsistentVersionWarning)
            obj = joblib.load(f)
        saved = getattr(obj, "_sklearn_version", None)
        print(f"• {f}\n   saved={saved}  type={type(obj).__name__}")
        if hasattr(obj, "steps"):
            for name, step in obj.steps:
                print(f"     - step '{name}': {type(step).__name__} saved={getattr(step, '_sklearn_version', None)}")
    except Exception as e:
        print(f"• {f}\n   ERROR: {e}")
PY

