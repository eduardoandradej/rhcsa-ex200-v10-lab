#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "== Python syntax (in-memory, no __pycache__) =="
python3 - <<'PY'
from pathlib import Path
for p in sorted(list(Path('labctl').glob('*.py')) + list(Path('labs').glob('*/*/grade.py'))):
    compile(p.read_text(), str(p), 'exec')
    print(f'OK {p}')
PY

echo "== Shell syntax =="
while IFS= read -r s; do bash -n "$s"; echo "OK ${s#"$ROOT"/}"; done < <(find "$ROOT/tests" -maxdepth 2 -type f -name '*.sh' | sort)

echo "== YAML catalog and ready-lab contract =="
python3 - <<'PY'
from pathlib import Path
import yaml
required={'id','title','objective','target','difficulty','duration','compatibility'}
ready=('setup.yml','finish.yml','grade.py','prompt.pt.md','prompt.en.md','solution.md')
for p in sorted(Path('labs').glob('*/*/lab.yml')):
    d=yaml.safe_load(p.read_text()) or {}; missing=required-set(d)
    if missing: raise SystemExit(f'{p}: missing {sorted(missing)}')
    status=d.get('status','catalog-only')
    if status=='ready':
        for name in ready:
            if not (p.parent/name).is_file(): raise SystemExit(f"{d['id']}: ready but missing {name}")
    print(f"OK {d['id']}: {status}")
PY

echo "== Grader CLI contract =="
python3 - <<'PY'
from pathlib import Path
import ast
bad=[]
for p in sorted(Path('labs').glob('*/*/grade.py')):
    tree=ast.parse(p.read_text(),filename=str(p)); ok=False
    for n in ast.walk(tree):
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='add_argument':
            if any(isinstance(a,ast.Constant) and a.value=='--json' for a in n.args): ok=True; break
    if not ok: bad.append(str(p))
    else: print(f'OK {p.parent.name}/grade.py: --json')
if bad: raise SystemExit('Graders sem --json:\n  '+'\n  '.join(bad))
PY

echo "== Ansible syntax =="
cd "$ROOT/ansible"
for p in prepare-objective*.yml; do
    [[ -f "$p" ]] || continue
    ansible-playbook --syntax-check "$p" >/dev/null
    echo "OK ansible/$p"
done
while IFS= read -r p; do ansible-playbook --syntax-check "$p" >/dev/null; echo "OK ${p#"$ROOT"/}"; done < <(find "$ROOT/labs" \( -name setup.yml -o -name finish.yml \) -type f | sort)

echo "== CLI smoke =="
cd "$ROOT"
"$ROOT/bin/lab" --version
"$ROOT/bin/lab" list >/dev/null

echo
echo "RELEASE GATE: PASS"
