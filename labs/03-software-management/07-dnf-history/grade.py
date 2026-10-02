#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json,subprocess

root=Path("/home/student/rhcsa-lab/obj03-07/output")
def txt(name):
    p=root/name
    return p.read_text(errors="replace") if p.is_file() else ""

installed=subprocess.run(["rpm","-q","rhcsa-history"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0

checks=[
 {"label":"histórico após instalação foi salvo","pass":"rhcsa-history" in txt("history-after-install.txt"),"hint":"Use dnf history list rhcsa-history."},
 {"label":"histórico após remoção foi salvo","pass":"rhcsa-history" in txt("history-after-remove.txt"),"hint":"Salve o histórico novamente após remover."},
 {"label":"detalhes da última transação foram salvos","pass":"rhcsa-history" in txt("last-transaction.txt") and ("Command Line" in txt("last-transaction.txt") or "Command line" in txt("last-transaction.txt")),"hint":"Use dnf history info <ID>."},
 {"label":"rhcsa-history está removido ao final","pass":not installed,"hint":"Remova o pacote com dnf."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj03-07","checks":checks,"score":score},ensure_ascii=False))
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
