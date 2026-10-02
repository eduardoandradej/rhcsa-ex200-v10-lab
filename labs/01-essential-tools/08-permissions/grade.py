#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json
import stat

root = Path("/home/student/rhcsa-lab/obj01-08")

def mode(path):
    if not path.exists():
        return None
    return stat.S_IMODE(path.stat().st_mode)

checks = [
    {
        "label": "report.txt possui modo 0640",
        "pass": mode(root / "data/report.txt") == 0o640,
        "hint": "Revise as permissões de proprietário, grupo e outros.",
    },
    {
        "label": "diretório scripts possui modo 0750",
        "pass": mode(root / "data/scripts") == 0o750,
        "hint": "Diretórios precisam de x para permitir travessia.",
    },
    {
        "label": "backup.sh recebeu execução somente para o proprietário",
        "pass": mode(root / "data/scripts/backup.sh") == 0o744,
        "hint": "Preserve as permissões existentes e adicione x ao usuário.",
    },
    {
        "label": "new-file.txt reflete umask 0027",
        "pass": mode(root / "generated/new-file.txt") == 0o640,
        "hint": "Arquivo regular parte de 0666 antes da aplicação da umask.",
    },
    {
        "label": "new-dir reflete umask 0027",
        "pass": mode(root / "generated/new-dir") == 0o750,
        "hint": "Diretório parte de 0777 antes da aplicação da umask.",
    },
]

score = round(sum(1 for c in checks if c["pass"]) / len(checks) * 100)
print(json.dumps({"lab_id": "obj01-08", "checks": checks, "score": score}, ensure_ascii=False))
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
