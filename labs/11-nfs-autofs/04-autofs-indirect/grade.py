#!/usr/bin/env python3
import argparse,json
from labctl.remote import json_from_remote_python
REMOTE_CHECKER=r"""
from pathlib import Path
import subprocess,json
root=Path("/home/student/rhcsa-lab/obj11-04/output")
def read(n):
 p=root/n; return p.read_text(errors="replace").strip() if p.is_file() else ""
def run(args):
 p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE); return p.returncode,p.stdout.strip()
master=Path("/etc/auto.master.d/rhcsa11.autofs").read_text(errors="replace") if Path("/etc/auto.master.d/rhcsa11.autofs").is_file() else ""
mapf=Path("/etc/auto.rhcsa11").read_text(errors="replace") if Path("/etc/auto.rhcsa11").is_file() else ""
svc_rc,_=run(["systemctl","is-active","--quiet","autofs"])
content=read("content.txt"); fm=read("findmnt.txt")
checks=[
 {"label":"mapa mestre indireto está correto","pass":"/remote11 /etc/auto.rhcsa11" in master,"hint":"Associe /remote11 ao mapa."},
 {"label":"wildcard e substituição & estão corretos","pass":"*" in mapf and "serverb:/srv/rhcsa11/projects/&" in mapf and "rw" in mapf and "sync" in mapf,"hint":"Use * e & no mapa indireto."},
 {"label":"autofs está ativo","pass":svc_rc==0,"hint":"Inicie autofs."},
 {"label":"alpha e beta foram montados sob demanda","pass":"serverb:/srv/rhcsa11/projects/alpha" in fm and "serverb:/srv/rhcsa11/projects/beta" in fm,"hint":"Acesse ambos os diretórios e salve findmnt."},
 {"label":"conteúdo das duas chaves foi validado","pass":"OBJ11 alpha project" in content and "OBJ11 beta project" in content,"hint":"Leia info.txt em alpha e beta."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj11-04","checks":checks,"score":score},ensure_ascii=False))
"""
def main():
 p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
 r=json_from_remote_python("servera",REMOTE_CHECKER); print(json.dumps(r,ensure_ascii=False)); return 0 if r["score"]==100 else 1
if __name__=="__main__": raise SystemExit(main())
