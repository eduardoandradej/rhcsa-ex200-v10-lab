#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json, subprocess

root=Path("/home/student/rhcsa-lab/obj05-08/output")

def number(name):
    try:
        return int((root/name).read_text().strip())
    except Exception:
        return 0

def run(args):
    p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return p.returncode,p.stdout.strip()

p1=number("start.pid")
p2=number("restart.pid")
p3=number("reload.pid")
_,current=run(["systemctl","show","-p","MainPID","--value","rhcsa-control.service"])
rc_active,active=run(["systemctl","is-active","rhcsa-control.service"])
rc_enabled,enabled=run(["systemctl","is-enabled","rhcsa-control.service"])

checks=[
 {"label":"PID inicial foi registrado","pass":p1>1,"hint":"Use systemctl show -p MainPID --value."},
 {"label":"restart alterou o MainPID","pass":p2>1 and p2!=p1,"hint":"Execute systemctl restart antes de registrar o segundo PID."},
 {"label":"reload preservou o MainPID","pass":p3==p2 and p3>1,"hint":"Execute systemctl reload; o PID principal deve permanecer."},
 {"label":"ExecReload foi realmente executado","pass":Path("/run/rhcsa-control.reload").is_file(),"hint":"O reload deve executar a ação definida na unit."},
 {"label":"serviço está ativo e continua desabilitado","pass":rc_active==0 and active=="active" and enabled=="disabled" and str(p3)==current,"hint":"Deixe ativo, mas não habilitado no boot."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj05-08","checks":checks,"score":score},ensure_ascii=False))
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
