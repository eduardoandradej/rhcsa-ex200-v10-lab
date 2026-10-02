#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json,os,subprocess,tempfile
root=Path("/home/student/rhcsa-lab/obj04-06")
script=root/"fileloop.sh"

def run(arg=None):
    cmd=[str(script)]
    if arg is not None: cmd.append(arg)
    try:
        p=subprocess.run(cmd,cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=5)
        return p.returncode,p.stdout,p.stderr
    except Exception:
        return 99,"",""

r_base=run("assets/services.list") if script.is_file() else (99,"","")
alt=root/"assets/alternate.list"
alt.write_text("alpha\n\nbeta\ngamma\n")
r_alt=run("assets/alternate.list") if script.is_file() else (99,"","")
r_missing=run("assets/missing.list") if script.is_file() else (99,"","")
r_none=run() if script.is_file() else (99,"","")

checks=[
 {"label":"fileloop.sh existe e é executável","pass":script.is_file() and os.access(script,os.X_OK),"hint":"Crie e torne o script executável."},
 {"label":"arquivo fornecido é processado em ordem","pass":r_base==(0,"ITEM:sshd\nITEM:chronyd\nITEM:firewalld\n",""),"hint":"Percorra o conteúdo do arquivo."},
 {"label":"arquivo alternativo também funciona e ignora linhas vazias","pass":r_alt==(0,"ITEM:alpha\nITEM:beta\nITEM:gamma\n",""),"hint":"Não fixe os itens do arquivo original."},
 {"label":"arquivo ausente retorna exit 1","pass":r_missing==(1,"MISSING-FILE:assets/missing.list\n",""),"hint":"Teste a existência do arquivo."},
 {"label":"falta de argumento retorna usage e exit 2","pass":r_none==(2,"","Usage: fileloop.sh FILE\n"),"hint":"Valide o parâmetro de entrada."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj04-06","checks":checks,"score":score},ensure_ascii=False))
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
