#!/usr/bin/env python3
import argparse, json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json, subprocess

root = Path("/home/student/rhcsa-lab/obj02-01/output")

def run(*args):
    p = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.stdout if p.returncode == 0 else None

def exact(name, expected):
    p = root / name
    return expected is not None and p.is_file() and p.read_text() == expected

passwd = run("getent", "passwd", "acctalpha")
fields = None
if passwd:
    f = passwd.rstrip("\n").split(":")
    fields = ":".join([f[0], f[2], f[3], f[5], f[6]]) + "\n"

checks = [
 {"label":"id de acctalpha foi consultado","pass":exact("acctalpha-id.txt", run("id","acctalpha")),"hint":"Use id acctalpha."},
 {"label":"entrada passwd de acctbeta foi consultada","pass":exact("acctbeta-passwd.txt", run("getent","passwd","acctbeta")),"hint":"Use getent passwd."},
 {"label":"entrada group de auditgrp foi consultada","pass":exact("auditgrp-group.txt", run("getent","group","auditgrp")),"hint":"Use getent group."},
 {"label":"campos essenciais de acctalpha estão corretos","pass":exact("acctalpha-fields.txt", fields),"hint":"Extraia nome, UID, GID, home e shell da entrada passwd."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj02-01","checks":checks,"score":score},ensure_ascii=False))
"""
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.parse_args()
    payload=json_from_remote_python("servera",REMOTE_CHECKER)
    print(json.dumps(payload,ensure_ascii=False))
    return 0 if payload["score"]==100 else 1
if __name__=="__main__": raise SystemExit(main())
