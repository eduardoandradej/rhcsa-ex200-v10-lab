#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json, subprocess

root=Path("/home/student/rhcsa-lab/obj03-03/output")
def txt(name):
    p=root/name
    return p.read_text(errors="replace") if p.is_file() else ""

installed=subprocess.run(["rpm","-q","rhcsa-toolkit"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0
checks=[
 {"label":"dnf search localizou rhcsa-toolkit","pass":"rhcsa-toolkit" in txt("search.txt"),"hint":"Use dnf search toolkit."},
 {"label":"dnf info retornou detalhes do pacote","pass":"rhcsa-toolkit" in txt("info.txt") and "1.0" in txt("info.txt"),"hint":"Use dnf info."},
 {"label":"dnf provides identificou o fornecedor do arquivo","pass":"rhcsa-toolkit" in txt("provider.txt"),"hint":"Use dnf provides com o caminho completo."},
 {"label":"dnf list exibiu a versão disponível","pass":"rhcsa-toolkit" in txt("list.txt") and "1.0-1" in txt("list.txt"),"hint":"Use dnf list."},
 {"label":"pacote permaneceu não instalado","pass":not installed,"hint":"Não instale o pacote neste exercício."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj03-03","checks":checks,"score":score},ensure_ascii=False))
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
