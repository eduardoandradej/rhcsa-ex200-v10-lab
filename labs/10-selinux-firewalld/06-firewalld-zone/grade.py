#!/usr/bin/env python3
import argparse,json
from labctl.remote import json_from_remote_python
REMOTE_CHECKER=r"""
from pathlib import Path
import subprocess,json
root=Path("/home/student/rhcsa-lab/obj10-06/output")
def run(args):
 p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE); return p.returncode,p.stdout.strip()
def yes(args):
 rc,out=run(args); return rc==0 and out.strip()=="yes"
checks=[
 {"label":"origem existe em runtime","pass":yes(["sudo","-n","firewall-cmd","--zone=rhcsa10","--query-source=198.51.100.0/24"]),"hint":"Adicione a origem e recarregue."},
 {"label":"serviço http existe em runtime","pass":yes(["sudo","-n","firewall-cmd","--zone=rhcsa10","--query-service=http"]),"hint":"Adicione o serviço http."},
 {"label":"porta 45100/tcp existe em runtime","pass":yes(["sudo","-n","firewall-cmd","--zone=rhcsa10","--query-port=45100/tcp"]),"hint":"Adicione 45100/tcp."},
 {"label":"regras estão persistentes","pass":all([
   yes(["sudo","-n","firewall-cmd","--permanent","--zone=rhcsa10","--query-source=198.51.100.0/24"]),
   yes(["sudo","-n","firewall-cmd","--permanent","--zone=rhcsa10","--query-service=http"]),
   yes(["sudo","-n","firewall-cmd","--permanent","--zone=rhcsa10","--query-port=45100/tcp"])
 ]),"hint":"Use --permanent e depois --reload."},
 {"label":"evidências runtime e permanente foram salvas","pass":(root/"runtime.txt").is_file() and (root/"permanent.txt").is_file() and "45100/tcp" in (root/"runtime.txt").read_text(errors="replace") and "45100/tcp" in (root/"permanent.txt").read_text(errors="replace"),"hint":"Salve os dois list-all."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj10-06","checks":checks,"score":score},ensure_ascii=False))
"""
def main():
 p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
 r=json_from_remote_python("servera",REMOTE_CHECKER); print(json.dumps(r,ensure_ascii=False)); return 0 if r["score"]==100 else 1
if __name__=="__main__": raise SystemExit(main())
