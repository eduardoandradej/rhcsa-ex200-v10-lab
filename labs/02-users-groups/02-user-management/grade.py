#!/usr/bin/env python3
import argparse, json
from labctl.remote import json_from_remote_python
REMOTE_CHECKER=r"""
import json, pwd
from pathlib import Path

def user(name):
    try: return pwd.getpwnam(name)
    except KeyError: return None

a=user("opsalpha"); b=user("opsbeta"); t=user("opstemp")
checks=[
 {"label":"opsalpha possui UID, comentário e shell solicitados","pass":bool(a and a.pw_uid==2301 and a.pw_gecos=="Operations Alpha" and a.pw_shell=="/bin/bash"),"hint":"Revise useradd/usermod de opsalpha."},
 {"label":"opsbeta possui comentário solicitado","pass":bool(b and b.pw_gecos=="Operations Beta"),"hint":"Revise o campo comment de opsbeta."},
 {"label":"opsbeta usa /srv/opsbeta como home","pass":bool(b and b.pw_dir=="/srv/opsbeta" and Path("/srv/opsbeta").is_dir()),"hint":"Use usermod -d com movimentação do home."},
 {"label":"opstemp foi removido com o home","pass":t is None and not Path("/home/opstemp").exists(),"hint":"Remova a conta e os dados pessoais."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj02-02","checks":checks,"score":score},ensure_ascii=False))
"""
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.parse_args()
    p=json_from_remote_python("servera",REMOTE_CHECKER); print(json.dumps(p,ensure_ascii=False)); return 0 if p["score"]==100 else 1
if __name__=="__main__": raise SystemExit(main())
