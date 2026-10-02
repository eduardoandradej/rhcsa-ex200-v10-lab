#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from labctl.remote import json_from_remote_python


REMOTE_CHECKER = r"""
from pathlib import Path
import json

root = Path("/home/student/rhcsa-lab/obj01-06")

expected_conf = (
    "# RHCSA training application\n"
    "environment=production\n"
    "workers=8\n"
    "logging=verbose\n"
    "port=8080\n"
)
expected_notes = (
    "review completed\n"
    "configuration updated\n"
    "ready for validation\n"
)

checks = [
    {
        "label": "app.conf possui a configuração final esperada",
        "pass": (root / "app.conf").is_file() and (root / "app.conf").read_text() == expected_conf,
        "hint": "Revise ordem, valores e remoção da linha debug=true.",
    },
    {
        "label": "notes.txt possui exatamente as três linhas solicitadas",
        "pass": (root / "notes.txt").is_file() and (root / "notes.txt").read_text() == expected_notes,
        "hint": "Revise conteúdo e quebras de linha de notes.txt.",
    },
]

score = round(sum(1 for c in checks if c["pass"]) / len(checks) * 100)
print(json.dumps({"lab_id": "obj01-06", "checks": checks, "score": score}, ensure_ascii=False))
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.parse_args()

    payload = json_from_remote_python("servera", REMOTE_CHECKER)
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload.get("score") == 100 else 1


if __name__ == "__main__":
    raise SystemExit(main())
