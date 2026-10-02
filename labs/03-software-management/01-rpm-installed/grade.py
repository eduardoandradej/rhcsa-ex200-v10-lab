#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json, subprocess

root=Path("/home/student/rhcsa-lab/obj03-01/output")
def run(args):
    p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return p.stdout if p.returncode==0 else None
def exact(name, expected):
    p=root/name
    return expected is not None and p.is_file() and p.read_text()==expected

checks=[
 {"label":"consulta do pacote openssh-clients está correta","pass":exact("package.txt",run(["rpm","-q","openssh-clients"])),"hint":"Use rpm -q."},
 {"label":"proprietário de /usr/bin/ssh foi identificado","pass":exact("owner.txt",run(["rpm","-qf","/usr/bin/ssh"])),"hint":"Use rpm -qf."},
 {"label":"arquivos de configuração foram listados","pass":exact("configs.txt",run(["rpm","-qc","openssh-clients"])),"hint":"Use rpm -qc."},
 {"label":"documentação do pacote foi listada","pass":exact("docs.txt",run(["rpm","-qd","openssh-clients"])),"hint":"Use rpm -qd."},
 {"label":"lista completa de arquivos foi produzida","pass":exact("files.txt",run(["rpm","-ql","openssh-clients"])),"hint":"Use rpm -ql."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj03-01","checks":checks,"score":score},ensure_ascii=False))
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
