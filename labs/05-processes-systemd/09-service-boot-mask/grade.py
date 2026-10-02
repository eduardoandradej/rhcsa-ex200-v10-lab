#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json, subprocess

root=Path("/home/student/rhcsa-lab/obj05-09/output")

def state(args):
    p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return p.stdout.strip()

boot_active=state(["systemctl","is-active","rhcsa-boot.service"])
boot_enabled=state(["systemctl","is-enabled","rhcsa-boot.service"])
blocked_active=state(["systemctl","is-active","rhcsa-blocked.service"])
blocked_enabled=state(["systemctl","is-enabled","rhcsa-blocked.service"])
deps=(root/"boot-dependencies.txt").read_text(errors="replace") if (root/"boot-dependencies.txt").is_file() else ""

checks=[
 {"label":"rhcsa-boot está ativo","pass":boot_active=="active","hint":"Inicie rhcsa-boot.service."},
 {"label":"rhcsa-boot está habilitado no boot","pass":boot_enabled=="enabled","hint":"Use systemctl enable."},
 {"label":"dependências foram registradas","pass":"rhcsa-boot.service" in deps and "network.target" in deps,"hint":"Use systemctl list-dependencies."},
 {"label":"rhcsa-blocked está inativo","pass":blocked_active!="active","hint":"Pare o serviço antes de mascará-lo."},
 {"label":"rhcsa-blocked está mascarado","pass":blocked_enabled=="masked","hint":"Use systemctl mask rhcsa-blocked.service."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj05-09","checks":checks,"score":score},ensure_ascii=False))
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
