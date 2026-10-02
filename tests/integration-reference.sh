#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ "$#" -eq 0 ]]; then
    LABS=(
        obj01-01 obj01-02 obj01-03 obj01-04 obj01-05
        obj01-06 obj01-07 obj01-08 obj01-09 obj01-10
    )
else
    LABS=("$@")
fi

cleanup_active() {
    if [[ -f "$ROOT/.state/active.json" ]]; then
        "$ROOT/bin/lab" finish >/dev/null 2>&1 || true
    fi
}
trap cleanup_active EXIT

fail_step() {
    local id="$1"
    local step="$2"
    local rc="$3"
    echo "REFERENCE TEST: FAIL ($id)"
    echo "Etapa que falhou: $step (rc=$rc)"
    exit "$rc"
}

for id in "${LABS[@]}"; do
    solver="$ROOT/tests/reference-solutions/${id}.sh"

    [[ -x "$solver" ]] || {
        echo "REFERENCE TEST: FAIL ($id)"
        echo "Etapa que falhou: reference solver ausente"
        exit 2
    }

    echo
    echo "===== $id ====="
    cleanup_active

    echo "[1/4] lab start"
    set +e
    start_output="$("$ROOT/bin/lab" start "$id" 2>&1)"
    start_rc=$?
    set -e
    if [[ "$start_rc" -ne 0 ]]; then
        printf '%s\n' "$start_output"
        fail_step "$id" "lab start" "$start_rc"
    fi
    echo "OK: lab start"

    echo "[2/4] reference solution"
    set +e
    solver_output="$("$solver" 2>&1)"
    solver_rc=$?
    set -e
    if [[ "$solver_rc" -ne 0 ]]; then
        printf '%s\n' "$solver_output"
        fail_step "$id" "reference solution" "$solver_rc"
    fi
    [[ -n "$solver_output" ]] && printf '%s\n' "$solver_output"
    echo "OK: reference solution"

    echo "[3/4] lab grade"
    set +e
    grade_output="$("$ROOT/bin/lab" grade "$id" 2>&1)"
    grade_rc=$?
    set -e

    printf '%s\n' "$grade_output"

    if [[ "$grade_rc" -ne 0 ]] || ! grep -q 'Score: 100%' <<<"$grade_output"; then
        fail_step "$id" "lab grade" "$grade_rc"
    fi

    echo "[4/4] lab finish"
    set +e
    finish_output="$("$ROOT/bin/lab" finish "$id" 2>&1)"
    finish_rc=$?
    set -e
    if [[ "$finish_rc" -ne 0 ]]; then
        printf '%s\n' "$finish_output"
        fail_step "$id" "lab finish" "$finish_rc"
    fi

    echo "REFERENCE TEST: PASS ($id)"
done

echo
echo "REFERENCE INTEGRATION: PASS"
