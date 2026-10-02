#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json,os,subprocess
root=Path("/home/student/rhcsa-lab/obj04-02")
script=root/"checkpath.sh"

def run(arg=None):
    cmd=[str(script)]
    if arg is not None: cmd.append(arg)
    try:
        p=subprocess.run(cmd,cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=5)
        return p.returncode,p.stdout,p.stderr
    except Exception:
        return 99,"",""

r_file=run("assets/config.ini") if script.is_file() else (99,"","")
r_dir=run("assets/data") if script.is_file() else (99,"","")
r_missing=run("assets/does-not-exist") if script.is_file() else (99,"","")
r_none=run() if script.is_file() else (99,"","")

checks=[
 {"label":"checkpath.sh existe e é executável","pass":script.is_file() and os.access(script,os.X_OK),"hint":"Crie e torne o script executável."},
 {"label":"arquivo regular é identificado","pass":r_file==(0,"FILE:assets/config.ini\n",""),"hint":"Teste se o caminho é arquivo regular."},
 {"label":"diretório é identificado","pass":r_dir==(0,"DIRECTORY:assets/data\n",""),"hint":"Teste se o caminho é diretório."},
 {"label":"caminho ausente retorna exit 1","pass":r_missing==(1,"MISSING:assets/does-not-exist\n",""),"hint":"Trate explicitamente o caminho inexistente."},
 {"label":"falta de argumento retorna usage e exit 2","pass":r_none==(2,"","Usage: checkpath.sh PATH\n"),"hint":"Valide $1 antes de testar o caminho."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj04-02","checks":checks,"score":score},ensure_ascii=False))
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
