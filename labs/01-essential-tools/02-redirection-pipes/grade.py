#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from labctl.remote import json_from_remote_python


REMOTE_CHECKER = r"""
from pathlib import Path
import json

root = Path("/home/student/rhcsa-lab/obj01-02")
out = root / "output"

expected_stdout = "INFO web01 ready\nINFO db01 ready\nINFO api01 ready\n"
expected_stderr = "WARN cache threshold\nERROR backup failed\n"
expected_combined = (
    "INFO web01 ready\n"
    "WARN cache threshold\n"
    "INFO db01 ready\n"
    "ERROR backup failed\n"
    "INFO api01 ready\n"
)
expected_append = "audit-check-complete\naudit-check-complete\n"
expected_unique = "NetworkManager\nchronyd\ncockpit\nfirewalld\nsshd\n"
expected_count = "4\n"

def exact(name, expected):
    path = out / name
    return path.is_file() and path.read_text() == expected

checks = [
    {
        "label": "stdout foi redirecionado separadamente",
        "pass": exact("stdout.log", expected_stdout),
        "hint": "stdout.log deve conter apenas as três linhas INFO.",
    },
    {
        "label": "stderr foi redirecionado separadamente",
        "pass": exact("stderr.log", expected_stderr),
        "hint": "stderr.log deve conter apenas WARN e ERROR.",
    },
    {
        "label": "stdout e stderr foram combinados no mesmo arquivo",
        "pass": exact("combined.log", expected_combined),
        "hint": "combined.log deve conter as cinco linhas emitidas por stream-demo.",
    },
    {
        "label": "append.log contém duas execuções acumuladas",
        "pass": exact("append.log", expected_append),
        "hint": "A segunda execução não deve sobrescrever a primeira.",
    },
    {
        "label": "pipeline produziu lista ordenada sem duplicatas",
        "pass": exact("services-unique.txt", expected_unique),
        "hint": "Ordene a entrada e elimine repetições.",
    },
    {
        "label": "pipeline contou corretamente as linhas active",
        "pass": exact("active-count.txt", expected_count),
        "hint": "active-count.txt deve conter apenas o número esperado.",
    },
]

score = round(sum(1 for c in checks if c["pass"]) / len(checks) * 100)
print(json.dumps({"lab_id": "obj01-02", "checks": checks, "score": score}, ensure_ascii=False))
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.parse_args()

    try:
        payload = json_from_remote_python("servera", REMOTE_CHECKER)
    except Exception as exc:
        print(str(exc))
        return 2

    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload.get("score") == 100 else 1


if __name__ == "__main__":
    raise SystemExit(main())
