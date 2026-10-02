#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json,os,subprocess
script=Path("/home/student/rhcsa-lab/obj04-05/argloop.sh")

def run(args):
    try:
        p=subprocess.run([str(script),*args],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=5)
        return p.returncode,p.stdout,p.stderr
    except Exception:
        return 99,"",""

r1=run(["alpha","beta gamma","delta"]) if script.is_file() else (99,"","")
r2=run(["one"]) if script.is_file() else (99,"","")
r0=run([]) if script.is_file() else (99,"","")

checks=[
 {"label":"argloop.sh existe e é executável","pass":script.is_file() and os.access(script,os.X_OK),"hint":"Crie e torne o script executável."},
 {"label":"loop preserva ordem e argumentos com espaços","pass":r1==(0,"ARG:alpha\nARG:beta gamma\nARG:delta\n",""),"hint":"Percorra os argumentos preservando cada item."},
 {"label":"uma única entrada também funciona","pass":r2==(0,"ARG:one\n",""),"hint":"Não dependa de quantidade fixa de parâmetros."},
 {"label":"zero argumentos retorna NO-ARGS e exit 1","pass":r0==(1,"NO-ARGS\n",""),"hint":"Trate a lista vazia antes do loop."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj04-05","checks":checks,"score":score},ensure_ascii=False))
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
