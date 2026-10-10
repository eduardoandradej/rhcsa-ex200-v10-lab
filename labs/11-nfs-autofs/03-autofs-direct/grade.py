#!/usr/bin/env python3
import argparse,json
from labctl.remote import json_from_remote_python
REMOTE_CHECKER=r"""
from pathlib import Path
import subprocess,json
root=Path("/home/student/rhcsa-lab/obj11-03/output")
def read(n):
 p=root/n; return p.read_text(errors="replace").strip() if p.is_file() else ""
def run(args):
 p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE); return p.returncode,p.stdout.strip()
master=Path("/etc/auto.master.d/rhcsa11.autofs").read_text(errors="replace") if Path("/etc/auto.master.d/rhcsa11.autofs").is_file() else ""
mapf=Path("/etc/auto.rhcsa11").read_text(errors="replace") if Path("/etc/auto.rhcsa11").is_file() else ""
svc_rc,_=run(["systemctl","is-active","--quiet","autofs"])
ena_rc,_=run(["systemctl","is-enabled","--quiet","autofs"])
# trigger if student forgot only the evidence? grader should not solve; do not access path here.
fm=read("findmnt.txt")
checks=[
 {"label":"mapa mestre direto está correto","pass":"/- /etc/auto.rhcsa11" in master,"hint":"Use /- no mapa mestre."},
 {"label":"mapa direto contém origem, destino e opções","pass":"/home/student/direct11" in mapf and "serverb:/srv/rhcsa11/direct" in mapf and "rw" in mapf and "sync" in mapf,"hint":"Configure o caminho absoluto no mapa direto."},
 {"label":"autofs está ativo e habilitado","pass":svc_rc==0 and ena_rc==0,"hint":"Use systemctl enable --now autofs."},
 {"label":"acesso disparou a montagem NFS","pass":"serverb:/srv/rhcsa11/direct" in fm and "nfs" in fm,"hint":"Acesse hello.txt e salve findmnt -T."},
 {"label":"conteúdo remoto foi validado","pass":read("content.txt")=="OBJ11 direct autofs" and read("service.txt")=="active","hint":"Acesse o conteúdo pelo ponto automático."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj11-03","checks":checks,"score":score},ensure_ascii=False))
"""
def main():
 p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
 r=json_from_remote_python("servera",REMOTE_CHECKER); print(json.dumps(r,ensure_ascii=False)); return 0 if r["score"]==100 else 1
if __name__=="__main__": raise SystemExit(main())
