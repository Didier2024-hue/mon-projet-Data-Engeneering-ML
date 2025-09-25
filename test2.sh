docker exec -i fastapi-cde python - <<'PY'
import os, glob, joblib, warnings
from sklearn.exceptions import InconsistentVersionWarning
from sklearn import __version__ as runtime

roots = [os.getenv("DATA_MODEL") or "/app/data/model", "/app/data/model", "/app"]
print("Runtime scikit-learn:", runtime)

cands = []
for root in roots:
    if not os.path.isdir(root): 
        continue
    for ext in ("*.pkl","*.joblib","*.sav","*.pkl.gz"):
        cands += [p for p in glob.glob(os.path.join(root,"**",ext), recursive=True) if os.path.isfile(p)]
cands = sorted(set(cands))

if not cands:
    print("Aucun artefact trouvé.")
for f in cands:
    try:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always", InconsistentVersionWarning)
            obj = joblib.load(f)
        saved = getattr(obj, "_sklearn_version", None)
        t = type(obj).__name__
        print(f"\n• {f}\n   saved={saved}  type={t}")
        if hasattr(obj,"steps"):
            for n, s in obj.steps:
                sv = getattr(s, "_sklearn_version", None)
                print(f"   - step '{n}': {type(s).__name__} saved={sv}")
        for warn in w:
            if issubclass(warn.category, InconsistentVersionWarning):
                print("   !! InconsistentVersionWarning:", str(warn.message).splitlines()[0])
    except Exception as e:
        print(f"\n• {f}\n   ERROR:", e)
PY

