#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json
import os
import stat
import subprocess
import tarfile

root = Path("/home/student/rhcsa-lab/obj01-10")
work = root / "work"

expected_report = (
    "INCIDENT=RHCSA-042\n"
    "OWNER=student\n"
    "STATUS=READY\n"
    "CLASSIFICATION=internal\n"
)

expected_prod = (
    "SRV-101|web01|prod|active|192.168.10.11\n"
    "SRV-103|db01|prod|active|192.168.10.21\n"
    "SRV-105|cache01|prod|active|192.168.10.41\n"
)

expected_alerts = (
    "WARN cache threshold reached\n"
    "ERROR backup failed\n"
)

def exact(path, expected):
    return path.is_file() and path.read_text() == expected

def mode(path):
    if not path.exists():
        return None
    return stat.S_IMODE(path.stat().st_mode)

report = work / "reports/final-report.txt"
hard = work / "links/report.hard"
sym = work / "links/alerts.current"
archive = work / "archive/evidence.tar.gz"

hard_ok = (
    report.is_file()
    and hard.is_file()
    and report.stat().st_ino == hard.stat().st_ino
)

sym_ok = (
    sym.is_symlink()
    and os.readlink(sym) == "../logs/alerts.log"
    and sym.resolve() == (work / "logs/alerts.log").resolve()
)

archive_ok = False
if archive.is_file():
    try:
        with tarfile.open(archive, "r:gz") as tf:
            names = set(tf.getnames())
            required = {
                "reports/final-report.txt",
                "reports/prod-active.txt",
                "reports/remote-host.txt",
                "logs/alerts.log",
            }
            archive_ok = required.issubset(names)
    except (tarfile.TarError, OSError):
        pass

man_proc = subprocess.run(
    ["man", "-w", "chmod"],
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    check=False,
)

checks = [
    {
        "label": "árvore work foi criada",
        "pass": all((work / d).is_dir() for d in ("reports", "logs", "links", "archive")),
        "hint": "Crie todos os subdiretórios solicitados.",
    },
    {
        "label": "report foi copiado e editado corretamente",
        "pass": exact(report, expected_report) and exact(root / "input/report.txt", expected_report.replace("READY", "PENDING")),
        "hint": "O original deve permanecer PENDING e a cópia deve ficar READY.",
    },
    {
        "label": "filtro prod + active está correto",
        "pass": exact(work / "reports/prod-active.txt", expected_prod),
        "hint": "Selecione somente registros que satisfaçam as duas condições.",
    },
    {
        "label": "filtro WARN ou ERROR está correto",
        "pass": exact(work / "logs/alerts.log", expected_alerts),
        "hint": "Use alternância com expressão regular estendida.",
    },
    {
        "label": "FQDN remoto do serverb foi registrado",
        "pass": exact(work / "reports/remote-host.txt", "serverb.lab.test\n"),
        "hint": "Obtenha hostname -f via SSH.",
    },
    {
        "label": "permissões solicitadas foram aplicadas",
        "pass": mode(report) == 0o640 and mode(work / "reports") == 0o750,
        "hint": "Revise os modos de final-report.txt e reports.",
    },
    {
        "label": "hard link do relatório é válido",
        "pass": hard_ok,
        "hint": "report.hard deve compartilhar o inode do relatório.",
    },
    {
        "label": "symbolic link dos alerts é válido",
        "pass": sym_ok,
        "hint": "Use o alvo relativo ../logs/alerts.log.",
    },
    {
        "label": "archive evidence.tar.gz é válido",
        "pass": archive_ok,
        "hint": "O archive deve conter reports e logs.",
    },
    {
        "label": "documentação local de chmod foi localizada",
        "pass": man_proc.returncode == 0 and exact(work / "reports/chmod-manpath.txt", man_proc.stdout),
        "hint": "Use man -w chmod.",
    },
]

score = round(sum(1 for c in checks if c["pass"]) / len(checks) * 100)
print(json.dumps({"lab_id": "obj01-10", "checks": checks, "score": score}, ensure_ascii=False))
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
