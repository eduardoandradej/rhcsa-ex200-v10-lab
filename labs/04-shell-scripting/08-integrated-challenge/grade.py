#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json,os,pwd,subprocess

root=Path("/home/student/rhcsa-lab/obj04-08")
script=root/"account-audit.sh"
hostname=subprocess.run(["hostname","-s"],text=True,stdout=subprocess.PIPE).stdout.strip()

def user_line(name):
    try:
        u=pwd.getpwnam(name)
        uid=u.pw_uid
        if uid==0:
            typ="PRIVILEGED"
        elif uid<1000:
            typ="SYSTEM"
        else:
            typ="REGULAR"
        return f"USER:{name}:UID={uid}:TYPE={typ}", True
    except KeyError:
        return f"USER:{name}:MISSING", False

def expected(names):
    rows=[f"HOST={hostname}"]
    total=found=missing=0
    for name in names:
        if not name:
            continue
        total+=1
        line,ok=user_line(name)
        rows.append(line)
        if ok: found+=1
        else: missing+=1
    rows.append(f"SUMMARY:TOTAL={total}:FOUND={found}:MISSING={missing}")
    return "\n".join(rows)+"\n"

def run(args):
    try:
        p=subprocess.run(
            [str(script),*args],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=8,
        )
        return p.returncode,p.stdout,p.stderr
    except Exception:
        return 99,"",""

base_names=["root","student","nobody","rhcsa-missing-user"]
r_base=run(["assets/users.list","output/report.txt"]) if script.is_file() else (99,"","")
report=(root/"output/report.txt").read_text(errors="replace") if (root/"output/report.txt").is_file() else ""

alt=root/"assets/grader-users.list"
alt.write_text("student\n\nroot\nrhcsa-another-missing\n")
r_alt=run(["assets/grader-users.list","output/grader-report.txt"]) if script.is_file() else (99,"","")
alt_report=(root/"output/grader-report.txt").read_text(errors="replace") if (root/"output/grader-report.txt").is_file() else ""

r_missing=run(["assets/no-file.list","output/x.txt"]) if script.is_file() else (99,"","")
r_args=run(["assets/users.list"]) if script.is_file() else (99,"","")

checks=[
 {"label":"account-audit.sh existe e é executável","pass":script.is_file() and os.access(script,os.X_OK),"hint":"Crie o script e aplique chmod +x."},
 {"label":"relatório principal está correto","pass":r_base==(0,"","") and report==expected(base_names),"hint":"Revise hostname, consulta de UID, classificação e contadores."},
 {"label":"script funciona com uma segunda lista criada pelo grader","pass":r_alt==(0,"","") and alt_report==expected(["student","root","rhcsa-another-missing"]),"hint":"Não fixe usuários ou totais no script."},
 {"label":"arquivo inexistente retorna mensagem e exit 1","pass":r_missing==(1,"MISSING-FILE:assets/no-file.list\n",""),"hint":"Valide INPUT_FILE."},
 {"label":"quantidade incorreta de argumentos retorna usage e exit 2","pass":r_args==(2,"","Usage: account-audit.sh INPUT_FILE OUTPUT_FILE\n"),"hint":"Valide os dois parâmetros posicionais."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj04-08","checks":checks,"score":score},ensure_ascii=False))
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.parse_args()

    payload = json_from_remote_python("serverb", REMOTE_CHECKER)
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload["score"] == 100 else 1

if __name__ == "__main__":
    raise SystemExit(main())
