#!/usr/bin/env python3
import argparse, json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import subprocess, json

root = Path("/home/student/rhcsa-lab/obj10-01/output")

def run(args):
    p = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.returncode, p.stdout.strip()

def read(name):
    p = root / name
    return p.read_text(errors="replace").strip() if p.is_file() else ""

_, mode = run(["getenforce"])
_, status = run(["sestatus"])
_, proc = run(["bash", "-lc", "ps -eZ | grep '[s]shd' || true"])
_, cfg = run(["ls", "-Z", "/etc/ssh/sshd_config"])

checks = [
    {"label":"modo SELinux registrado", "pass":read("getenforce.txt") == mode and mode in ("Enforcing","Permissive"), "hint":"Use getenforce."},
    {"label":"sestatus registrado", "pass":"SELinux status:" in read("sestatus.txt") and mode.lower() in read("sestatus.txt").lower(), "hint":"Use sestatus."},
    {"label":"contexto do processo sshd registrado", "pass":bool(proc) and "sshd" in read("sshd-process.txt") and ":" in read("sshd-process.txt"), "hint":"Use ps -eZ."},
    {"label":"contexto do sshd_config registrado", "pass":"/etc/ssh/sshd_config" in read("sshd-config.txt") and ":" in read("sshd-config.txt"), "hint":"Use ls -Z."},
    {"label":"arquivo de customizações locais criado", "pass":(root/"fcontext-local.txt").is_file(), "hint":"Use semanage fcontext -l -C."},
]
score = round(sum(c["pass"] for c in checks) / len(checks) * 100)
print(json.dumps({"lab_id":"obj10-01","checks":checks,"score":score}, ensure_ascii=False))
"""

def main():
    p=argparse.ArgumentParser(); p.add_argument("--json", action="store_true"); p.parse_args()
    r=json_from_remote_python("servera", REMOTE_CHECKER)
    print(json.dumps(r, ensure_ascii=False))
    return 0 if r["score"] == 100 else 1

if __name__ == "__main__":
    raise SystemExit(main())
