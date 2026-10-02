#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json, subprocess

root=Path("/home/student/rhcsa-lab/obj05-06/output")

def text(name):
    p=root/name
    return p.read_text(errors="replace") if p.is_file() else ""

p=subprocess.run(["tuned-adm","active"],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
active=p.stdout.strip()

checks=[
 {"label":"perfil recomendado foi consultado","pass":bool(text("recommended.txt").strip()),"hint":"Execute tuned-adm recommend."},
 {"label":"lista de perfis foi salva e contém throughput-performance","pass":"throughput-performance" in text("profiles.txt"),"hint":"Execute tuned-adm list."},
 {"label":"throughput-performance está ativo","pass":"throughput-performance" in active,"hint":"Use tuned-adm profile throughput-performance."},
 {"label":"estado ativo foi registrado","pass":"throughput-performance" in text("active.txt"),"hint":"Salve tuned-adm active."},
 {"label":"verificação do perfil foi executada","pass":bool(text("verify.txt").strip()),"hint":"Execute tuned-adm verify e salve a saída; o código de retorno é diagnóstico."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj05-06","checks":checks,"score":score},ensure_ascii=False))
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
