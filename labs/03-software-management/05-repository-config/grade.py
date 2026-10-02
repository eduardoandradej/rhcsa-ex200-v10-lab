#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import configparser,json,subprocess

repo=Path("/etc/yum.repos.d/rhcsa-custom.repo")
cfg=configparser.ConfigParser()
try:
    cfg.read(repo)
    sec=cfg["rhcsa-custom"]
except Exception:
    sec={}

p=subprocess.run(
    ["dnf","-q","--disablerepo=*","--enablerepo=rhcsa-custom","list","available","rhcsa-toolkit"],
    text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE
)
checks=[
 {"label":"arquivo de repositório existe","pass":repo.is_file(),"hint":"Crie /etc/yum.repos.d/rhcsa-custom.repo."},
 {"label":"ID e nome do repositório estão corretos","pass":bool(sec) and sec.get("name")=="RHCSA Custom Repository","hint":"Revise [rhcsa-custom] e name=."},
 {"label":"baseurl aponta para o repositório local","pass":bool(sec) and sec.get("baseurl")=="file:///var/lib/rhcsa-lab/obj03/repos/base","hint":"Revise baseurl=."},
 {"label":"repositório está habilitado e sem GPG check","pass":bool(sec) and sec.get("enabled")=="1" and sec.get("gpgcheck")=="0","hint":"Revise enabled e gpgcheck."},
 {"label":"DNF consegue consultar rhcsa-toolkit no repositório","pass":p.returncode==0 and "rhcsa-toolkit" in p.stdout,"hint":"Teste dnf list usando somente rhcsa-custom."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj03-05","checks":checks,"score":score},ensure_ascii=False))
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
