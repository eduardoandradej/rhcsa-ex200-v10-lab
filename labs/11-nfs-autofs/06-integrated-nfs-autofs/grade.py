#!/usr/bin/env python3
import argparse,json
from labctl.remote import json_from_remote_python
REMOTE_CHECKER=r"""
from pathlib import Path
import subprocess,json
root=Path("/home/student/rhcsa-lab/obj11-06/output")
def read(n):
 p=root/n; return p.read_text(errors="replace").strip() if p.is_file() else ""
def run(args):
 p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE); return p.returncode,p.stdout.strip()
master=Path("/etc/auto.master.d/rhcsa11.autofs").read_text(errors="replace") if Path("/etc/auto.master.d/rhcsa11.autofs").is_file() else ""
mapf=Path("/etc/auto.rhcsa11").read_text(errors="replace") if Path("/etc/auto.rhcsa11").is_file() else ""
svc_rc,_=run(["systemctl","is-active","--quiet","autofs"])
manual_rc,_=run(["findmnt","/mnt/rhcsa11-check"])
content=read("content.txt"); fm=read("findmnt.txt")
checks=[
 {"label":"montagem manual foi comprovada","pass":"serverb:/srv/rhcsa11/integrated" in read("manual.txt") and "red" in read("list.txt") and "hat" in read("list.txt"),"hint":"Valide manualmente antes do AutoFS."},
 {"label":"montagem manual foi desmontada","pass":manual_rc!=0,"hint":"Desmonte /mnt/rhcsa11-check."},
 {"label":"mapa indireto integrado está correto","pass":"/remote11-final /etc/auto.rhcsa11" in master and "*" in mapf and "serverb:/srv/rhcsa11/integrated/&" in mapf,"hint":"Configure o wildcard indireto."},
 {"label":"autofs permanece ativo","pass":svc_rc==0,"hint":"Use enable --now."},
 {"label":"red e hat foram montados sob demanda","pass":"serverb:/srv/rhcsa11/integrated/red" in fm and "serverb:/srv/rhcsa11/integrated/hat" in fm,"hint":"Acesse ambas as chaves."},
 {"label":"conteúdo remoto foi validado","pass":"OBJ11 RED team" in content and "OBJ11 HAT team" in content,"hint":"Leia os dois info.txt."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj11-06","checks":checks,"score":score},ensure_ascii=False))
"""
def main():
 p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
 r=json_from_remote_python("servera",REMOTE_CHECKER); print(json.dumps(r,ensure_ascii=False)); return 0 if r["score"]==100 else 1
if __name__=="__main__": raise SystemExit(main())
