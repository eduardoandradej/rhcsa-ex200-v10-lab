#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json,os,subprocess
script=Path("/home/student/rhcsa-lab/obj04-04/sysreport.sh")

def out(args):
    return subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.strip()

hostname=out(["hostname","-s"])
kernel=out(["uname","-r"])
bash_path=out(["bash","-lc","command -v bash"])
user_count=str(len(subprocess.run(["getent","passwd"],text=True,stdout=subprocess.PIPE).stdout.rstrip("\n").splitlines()))
expected=f"HOSTNAME={hostname}\nKERNEL={kernel}\nBASH_PATH={bash_path}\nUSER_COUNT={user_count}\n"

try:
    p=subprocess.run([str(script)],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=5) if script.is_file() else None
except Exception:
    p=None

checks=[
 {"label":"sysreport.sh existe e é executável","pass":script.is_file() and os.access(script,os.X_OK),"hint":"Crie e torne o script executável."},
 {"label":"relatório usa valores atuais do sistema","pass":bool(p and p.returncode==0 and p.stdout==expected and p.stderr==""),"hint":"Capture e processe a saída de hostname, uname, command -v e getent."},
 {"label":"saída possui exatamente quatro linhas","pass":bool(p and len(p.stdout.rstrip("\n").splitlines())==4),"hint":"Produza somente as quatro linhas solicitadas."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj04-04","checks":checks,"score":score},ensure_ascii=False))
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
