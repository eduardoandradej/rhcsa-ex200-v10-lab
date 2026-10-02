#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json,os,pwd,subprocess
script=Path("/home/student/rhcsa-lab/obj04-07/userreport.sh")

def expected(name):
    try:
        u=pwd.getpwnam(name)
        return f"USER:{name}:UID={u.pw_uid}:HOME={u.pw_dir}:SHELL={u.pw_shell}\n"
    except KeyError:
        return f"USER:{name}:MISSING\n"

def run(args):
    try:
        p=subprocess.run([str(script),*args],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=5)
        return p.returncode,p.stdout,p.stderr
    except Exception:
        return 99,"",""

names=["root","student","rhcsa-no-such-user"]
r1=run(names) if script.is_file() else (99,"","")
r2=run(["student","root"]) if script.is_file() else (99,"","")
r0=run([]) if script.is_file() else (99,"","")

exp1="".join(expected(n) for n in names)
exp2="".join(expected(n) for n in ["student","root"])

checks=[
 {"label":"userreport.sh existe e é executável","pass":script.is_file() and os.access(script,os.X_OK),"hint":"Crie e torne o script executável."},
 {"label":"usuários existentes e ausentes são processados dinamicamente","pass":r1==(0,exp1,""),"hint":"Use getent/passwd e extraia os campos necessários."},
 {"label":"ordem dos argumentos é preservada","pass":r2==(0,exp2,""),"hint":"Percorra a lista de argumentos em ordem."},
 {"label":"zero argumentos retorna NO-USERS e exit 1","pass":r0==(1,"NO-USERS\n",""),"hint":"Trate a entrada vazia antes do loop."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj04-07","checks":checks,"score":score},ensure_ascii=False))
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
