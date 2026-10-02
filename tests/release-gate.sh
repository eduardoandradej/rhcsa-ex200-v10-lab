#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "== Python syntax =="
python3 -m py_compile labctl/*.py
find labs -name grade.py -print0 | xargs -0 -r python3 -m py_compile

echo "== Shell syntax =="
while IFS= read -r script; do
    bash -n "$script"
    echo "OK ${script#"$ROOT"/}"
done < <(
    find "$ROOT/tests/reference-solutions" -type f -name '*.sh' | sort
)

bash -n "$ROOT/tests/integration-reference.sh"
bash -n "$ROOT/tests/integration-objective04.sh"
echo "OK tests/integration-reference.sh"
echo "OK tests/integration-objective04.sh"

echo "== YAML catalog and ready-lab contract =="
python3 - <<'PY'
from pathlib import Path
import yaml

required = {
    "id", "title", "objective", "target",
    "difficulty", "duration", "compatibility"
}
ready_files = (
    "setup.yml", "finish.yml", "grade.py",
    "prompt.pt.md", "prompt.en.md", "solution.md"
)

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

echo "== Grader CLI contract =="
python3 - <<'PY'
from pathlib import Path
import ast

failures = []

for path in sorted(Path("labs").glob("*/*/grade.py")):
    tree = ast.parse(path.read_text(), filename=str(path))
    has_json_option = False

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "add_argument":
                for arg in node.args:
                    if isinstance(arg, ast.Constant) and arg.value == "--json":
                        has_json_option = True
                        break
        if has_json_option:
            break

    if not has_json_option:
        failures.append(str(path))
    else:
        print(f"OK {path.parent.name}/grade.py: --json")

if failures:
    raise SystemExit(
        "Graders sem suporte ao contrato --json:\n  "
        + "\n  ".join(failures)
    )
PY

echo "== Ansible syntax =="
cd "$ROOT/ansible"

if [[ -f prepare-objective03.yml ]]; then
    ansible-playbook --syntax-check prepare-objective03.yml >/dev/null
    echo "OK ansible/prepare-objective03.yml"
fi

while IFS= read -r playbook; do
    ansible-playbook --syntax-check "$playbook" >/dev/null
    echo "OK $(basename "$(dirname "$playbook")")/$(basename "$playbook")"
done < <(
    find "$ROOT/labs" \( -name setup.yml -o -name finish.yml \) -type f | sort
)

echo "== CLI smoke =="
cd "$ROOT"
"$ROOT/bin/lab" --version
"$ROOT/bin/lab" list >/dev/null

echo
echo "RELEASE GATE: PASS"
