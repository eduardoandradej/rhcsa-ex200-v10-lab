#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
if [[ "$#" -eq 0 ]]; then
  echo "===== Full regression prerequisites ====="
  ( cd "$ROOT/ansible"; for p in prepare-objective03.yml prepare-objective05.yml prepare-objective06.yml prepare-objective07.yml; do [[ -f "$p" ]] && ansible-playbook "$p"; done )
  LABS=(
    obj01-01 obj01-02 obj01-03 obj01-04 obj01-05 obj01-06 obj01-07 obj01-08 obj01-09 obj01-10
    obj02-01 obj02-02 obj02-03 obj02-04 obj02-05 obj02-06 obj02-07 obj02-08
    obj03-01 obj03-02 obj03-03 obj03-04 obj03-05 obj03-06 obj03-07 obj03-08
    obj04-01 obj04-02 obj04-03 obj04-04 obj04-05 obj04-06 obj04-07 obj04-08
    obj05-01 obj05-02 obj05-03 obj05-04 obj05-05 obj05-06 obj05-07 obj05-08 obj05-09 obj05-10
    obj06-01 obj06-02 obj06-03 obj06-04 obj06-05 obj06-06 obj06-07 obj06-08
    obj07-01 obj07-02 obj07-03 obj07-04 obj07-05 obj07-06 obj07-07 obj07-08 )
else LABS=("$@"); fi
cleanup_active(){ if [[ -f "$ROOT/.state/active.json" ]]; then "$ROOT/bin/lab" finish >/dev/null 2>&1 || true; fi; }
trap cleanup_active EXIT
fail_step(){ local id="$1" step="$2" rc="$3"; echo "REFERENCE TEST: FAIL ($id)"; echo "Etapa que falhou: $step (rc=$rc)"; exit "$rc"; }
for id in "${LABS[@]}"; do
  solver="$ROOT/tests/reference-solutions/${id}.sh"; [[ -x "$solver" ]] || { echo "REFERENCE TEST: FAIL ($id)"; echo "Reference solver ausente"; exit 2; }
  echo; echo "===== $id ====="; cleanup_active
  echo "[1/4] lab start"; set +e; out="$("$ROOT/bin/lab" start "$id" 2>&1)"; rc=$?; set -e; [[ $rc -eq 0 ]] || { printf '%s\n' "$out"; fail_step "$id" "lab start" "$rc"; }; echo "OK: lab start"
  echo "[2/4] reference solution"; set +e; out="$("$solver" 2>&1)"; rc=$?; set -e; [[ $rc -eq 0 ]] || { printf '%s\n' "$out"; fail_step "$id" "reference solution" "$rc"; }; [[ -n "$out" ]] && printf '%s\n' "$out"; echo "OK: reference solution"
  echo "[3/4] lab grade"; set +e; out="$("$ROOT/bin/lab" grade "$id" 2>&1)"; rc=$?; set -e; printf '%s\n' "$out"; if [[ $rc -ne 0 ]] || ! grep -q 'Score: 100%' <<<"$out"; then fail_step "$id" "lab grade" "$rc"; fi
  echo "[4/4] lab finish"; set +e; out="$("$ROOT/bin/lab" finish "$id" 2>&1)"; rc=$?; set -e; [[ $rc -eq 0 ]] || { printf '%s\n' "$out"; fail_step "$id" "lab finish" "$rc"; }
  echo "REFERENCE TEST: PASS ($id)"
done
echo; echo "REFERENCE INTEGRATION: PASS"
