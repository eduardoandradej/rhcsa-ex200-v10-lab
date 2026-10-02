#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json, subprocess

root=Path("/home/student/rhcsa-lab/obj05-07/output")

def text(name):
    p=root/name
    return p.read_text(errors="replace") if p.is_file() else ""

def run(args):
    p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return p.stdout

active=run(["systemctl","is-active","sshd.service"])
enabled=run(["systemctl","is-enabled","sshd.service"])

checks=[
 {"label":"lista de service units foi produzida","pass":"sshd.service" in text("services.txt") and "chronyd.service" in text("services.txt"),"hint":"Use systemctl list-units --type=service --all --no-pager."},
 {"label":"lista de unit files foi produzida","pass":"sshd.service" in text("unit-files.txt") and "chronyd.service" in text("unit-files.txt"),"hint":"Use systemctl list-unit-files --type=service --no-pager."},
 {"label":"is-active do sshd está correto","pass":text("sshd-active.txt")==active,"hint":"Salve a saída de systemctl is-active sshd.service."},
 {"label":"is-enabled do sshd está correto","pass":text("sshd-enabled.txt")==enabled,"hint":"Salve a saída de systemctl is-enabled sshd.service."},
 {"label":"status do chronyd foi salvo","pass":"chronyd.service" in text("chronyd-status.txt") and ("Active:" in text("chronyd-status.txt")),"hint":"Use systemctl status chronyd.service --no-pager."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj05-07","checks":checks,"score":score},ensure_ascii=False))
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.parse_args()

    payload = json_from_remote_python("servera", REMOTE_CHECKER)
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload["score"] == 100 else 1

if __name__ == "__main__":
    raise SystemExit(main())
