#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import configparser,json,subprocess

p=subprocess.run(["rpm","-q","--qf","%{VERSION}-%{RELEASE}\n","rhcsa-update-demo"],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
cfg=configparser.ConfigParser()
cfg.read("/etc/yum.repos.d/rhcsa-update.repo")
base=cfg["rhcsa-base"] if cfg.has_section("rhcsa-base") else {}
err=cfg["rhcsa-errata"] if cfg.has_section("rhcsa-errata") else {}

checks=[
 {"label":"rhcsa-update-demo foi atualizado para 2.0-1","pass":p.returncode==0 and p.stdout.strip()=="2.0-1","hint":"Habilite errata e use dnf upgrade no pacote."},
 {"label":"rhcsa-base está desabilitado ao final","pass":bool(base) and base.get("enabled")=="0","hint":"Desabilite persistentemente rhcsa-base."},
 {"label":"rhcsa-errata está desabilitado ao final","pass":bool(err) and err.get("enabled")=="0","hint":"Desabilite persistentemente rhcsa-errata."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj03-06","checks":checks,"score":score},ensure_ascii=False))
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
