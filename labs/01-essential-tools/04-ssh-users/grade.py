#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from labctl.remote import json_from_remote_python


REMOTE_CHECKER = r"""
from pathlib import Path
import json
import subprocess

root = Path("/home/student/rhcsa-lab/obj01-04")
switched = "/home/labuser/switch-user.txt"

def exact(path, value):
    return path.is_file() and path.read_text() == value

def sudo_text(*args):
    proc = subprocess.run(
        ["sudo", "-n", *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return proc.returncode, proc.stdout

cat_rc, switched_content = sudo_text("cat", switched)
stat_rc, switched_owner = sudo_text("stat", "-c", "%U", switched)

checks = [
    {
        "label": "FQDN remoto do serverb foi registrado",
        "pass": exact(root / "remote-host.txt", "serverb.lab.test\n"),
        "hint": "Execute hostname -f remotamente por SSH e redirecione a saída localmente.",
    },
    {
        "label": "usuário remoto do serverb foi registrado",
        "pass": exact(root / "remote-user.txt", "student\n"),
        "hint": "Execute whoami remotamente por SSH.",
    },
    {
        "label": "troca para labuser produziu o resultado esperado",
        "pass": cat_rc == 0 and switched_content == "labuser\n",
        "hint": "Use uma shell de login do labuser e gere o arquivo como esse usuário.",
    },
    {
        "label": "arquivo de troca de usuário pertence ao labuser",
        "pass": stat_rc == 0 and switched_owner.strip() == "labuser",
        "hint": "O arquivo deve ser criado durante a sessão do labuser.",
    },
]

score = round(sum(1 for c in checks if c["pass"]) / len(checks) * 100)
print(json.dumps({"lab_id": "obj01-04", "checks": checks, "score": score}, ensure_ascii=False))
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.parse_args()

    try:
        payload = json_from_remote_python("servera", REMOTE_CHECKER)
    except Exception as exc:
        # Infrastructure/grader failures are errors, not INCOMPLETE results.
        raise RuntimeError(f"obj01-04 remote checker failed: {exc}") from exc

    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload.get("score") == 100 else 1


if __name__ == "__main__":
    raise SystemExit(main())
