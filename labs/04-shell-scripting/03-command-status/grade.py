#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json,os,subprocess
script=Path("/home/student/rhcsa-lab/obj04-03/checkcmd.sh")

def resolved(name):
    p=subprocess.run(["bash","-lc",f"command -v {name}"],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return p.stdout.strip()

def run(name=None):
    cmd=[str(script)]
    if name is not None: cmd.append(name)
    try:
        p=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=5)
        return p.returncode,p.stdout,p.stderr
    except Exception:
        return 99,"",""

ssh_path=resolved("ssh")
grep_path=resolved("grep")
r1=run("ssh") if script.is_file() else (99,"","")
r2=run("grep") if script.is_file() else (99,"","")
r3=run("rhcsa-command-that-does-not-exist") if script.is_file() else (99,"","")
r4=run() if script.is_file() else (99,"","")

checks=[
 {"label":"checkcmd.sh existe e é executável","pass":script.is_file() and os.access(script,os.X_OK),"hint":"Crie e torne o script executável."},
 {"label":"ssh é resolvido dinamicamente","pass":r1==(0,f"FOUND:ssh:{ssh_path}\n",""),"hint":"Use o status e a saída de command -v."},
 {"label":"outro comando válido também funciona","pass":r2==(0,f"FOUND:grep:{grep_path}\n",""),"hint":"Não fixe o resultado para um único comando."},
 {"label":"comando inexistente retorna exit 1","pass":r3==(1,"NOTFOUND:rhcsa-command-that-does-not-exist\n",""),"hint":"Trate o retorno de falha do comando de consulta."},
 {"label":"falta de argumento retorna exit 2","pass":r4==(2,"","Usage: checkcmd.sh COMMAND\n"),"hint":"Valide a entrada."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj04-03","checks":checks,"score":score},ensure_ascii=False))
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
