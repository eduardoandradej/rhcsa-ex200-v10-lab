#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json, os, subprocess

script=Path("/home/student/rhcsa-lab/obj04-01/greet.sh")

def run(args):
    try:
        p=subprocess.run(
            [str(script), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
        )
        return p.returncode,p.stdout,p.stderr
    except Exception:
        return 99,"",""

rc1,out1,err1=run(["alice","admin"]) if script.is_file() else (99,"","")
rc2,out2,err2=run(["bob","operations"]) if script.is_file() else (99,"","")
rc3,out3,err3=run(["onlyone"]) if script.is_file() else (99,"","")
rc4,out4,err4=run([]) if script.is_file() else (99,"","")

checks=[
 {"label":"greet.sh existe e é executável","pass":script.is_file() and os.access(script,os.X_OK),"hint":"Crie o arquivo e aplique chmod +x."},
 {"label":"dois parâmetros são processados corretamente","pass":rc1==0 and out1=="USER=alice ROLE=admin\n" and err1=="","hint":"Use os parâmetros posicionais do script."},
 {"label":"o script funciona com outra entrada válida","pass":rc2==0 and out2=="USER=bob ROLE=operations\n","hint":"Não fixe valores no script."},
 {"label":"quantidade inválida gera usage em stderr e exit 2","pass":rc3==2 and out3=="" and err3=="Usage: greet.sh USER ROLE\n","hint":"Valide a quantidade de parâmetros antes de processá-los."},
 {"label":"zero argumentos também é rejeitado","pass":rc4==2 and err4=="Usage: greet.sh USER ROLE\n","hint":"Teste a contagem de argumentos."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj04-01","checks":checks,"score":score},ensure_ascii=False))
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
