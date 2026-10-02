#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "== Python syntax =="
python3 -m py_compile labctl/*.py
find labs -name grade.py -print0 | xargs -0 -r python3 -m py_compile

echo "== YAML catalog and ready-lab contract =="
python3 - <<'PY'
from pathlib import Path
import yaml

required = {"id", "title", "objective", "target", "difficulty", "duration", "compatibility"}
ready_files = ("setup.yml", "finish.yml", "grade.py", "prompt.pt.md", "prompt.en.md", "solution.md")

for path in sorted(Path("labs").glob("*/*/lab.yml")):
    data = yaml.safe_load(path.read_text()) or {}
    missing = required - set(data)
    if missing:
        raise SystemExit(f"{path}: missing {sorted(missing)}")

    status = data.get("status", "catalog-only")
    if status == "ready":
        for name in ready_files:
            if not (path.parent / name).is_file():
                raise SystemExit(f"{data['id']}: ready but missing {name}")

    print(f"OK {data['id']}: {status}")
PY

echo "== Ansible syntax =="
cd "$ROOT/ansible"
while IFS= read -r playbook; do
    ansible-playbook --syntax-check "$playbook" >/dev/null
    echo "OK $(basename "$(dirname "$playbook")")/$(basename "$playbook")"
done < <(find "$ROOT/labs" \( -name setup.yml -o -name finish.yml \) -type f | sort)

echo "== CLI smoke =="
cd "$ROOT"
"$ROOT/bin/lab" --version
"$ROOT/bin/lab" list >/dev/null

echo
echo "RELEASE GATE: PASS"
