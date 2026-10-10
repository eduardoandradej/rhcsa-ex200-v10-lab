#!/usr/bin/env python3
import argparse, json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import subprocess, json, re

root=Path("/home/student/rhcsa-lab/obj10-02/output")
def read(n):
    p=root/n
    return p.read_text(errors="replace").strip() if p.is_file() else ""
def run(args):
    p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return p.returncode,p.stdout.strip()

_, mode=run(["getenforce"])
cfg=Path("/etc/selinux/config").read_text(errors="replace")
persistent=bool(re.search(r"(?m)^SELINUX=enforcing\s*$", cfg))
checks=[
 {"label":"SELinux atual está enforcing","pass":mode=="Enforcing","hint":"Use setenforce 1."},
 {"label":"SELinux persistente está enforcing","pass":persistent,"hint":"Configure SELINUX=enforcing."},
 {"label":"evidência do modo foi salva","pass":read("getenforce.txt")=="Enforcing","hint":"Grave getenforce."},
 {"label":"evidência da configuração foi salva","pass":"SELINUX=enforcing" in read("config.txt"),"hint":"Grave a linha SELINUX=."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj10-02","checks":checks,"score":score},ensure_ascii=False))
"""
def main():
    p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
    r=json_from_remote_python("servera",REMOTE_CHECKER); print(json.dumps(r,ensure_ascii=False))
    return 0 if r["score"]==100 else 1
if __name__=="__main__": raise SystemExit(main())
