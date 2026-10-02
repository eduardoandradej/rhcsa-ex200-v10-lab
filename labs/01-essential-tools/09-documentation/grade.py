#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json
import subprocess

root = Path("/home/student/rhcsa-lab/obj01-09/output")

def exact(name, expected):
    path = root / name
    return path.is_file() and path.read_text() == expected

def cmd(*args):
    proc = subprocess.run(
        list(args),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return proc.returncode, proc.stdout

rc_man, manpath = cmd("man", "-w", "chmod")
rc_rpm, rpm_docs = cmd("rpm", "-qd", "openssh-clients")

ssh_man = ""
if rc_rpm == 0:
    for line in rpm_docs.splitlines():
        if line.endswith("/ssh.1.gz") or line.endswith("/ssh.1"):
            ssh_man = line + "\n"
            break

checks = [
    {
        "label": "caminho da man page de chmod foi localizado",
        "pass": rc_man == 0 and exact("chmod-manpath.txt", manpath),
        "hint": "Use o próprio man para descobrir onde está a página.",
    },
    {
        "label": "seção de chmod foi identificada",
        "pass": exact("chmod-section.txt", "1\n"),
        "hint": "chmod é um comando de usuário.",
    },
    {
        "label": "seção do formato de /etc/passwd foi identificada",
        "pass": exact("passwd-section.txt", "5\n"),
        "hint": "Procure a página que documenta o formato do arquivo, não o comando passwd.",
    },
    {
        "label": "documentação ssh(1) do RPM foi localizada",
        "pass": bool(ssh_man) and exact("ssh-manpage.txt", ssh_man),
        "hint": "Consulte os arquivos de documentação instalados por openssh-clients.",
    },
    {
        "label": "opção curta de criação do tar foi identificada",
        "pass": exact("tar-create-option.txt", "-c\n"),
        "hint": "Consulte a página de manual do tar.",
    },
]

score = round(sum(1 for c in checks if c["pass"]) / len(checks) * 100)
print(json.dumps({"lab_id": "obj01-09", "checks": checks, "score": score}, ensure_ascii=False))
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
