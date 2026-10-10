#!/usr/bin/env python3
import argparse,json
from labctl.remote import json_from_remote_python
REMOTE_CHECKER=r"""
from pathlib import Path
import subprocess,json,re
root=Path("/home/student/rhcsa-lab/obj10-03/output")
def run(args):
 p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE); return p.returncode,p.stdout.strip()
def read(n):
 p=root/n; return p.read_text(errors="replace").strip() if p.is_file() else ""
_,d=run(["ls","-Zd","/srv/web10"])
_,f=run(["ls","-Z","/srv/web10/index.html"])
_,local=run(["sudo","-n","semanage","fcontext","-l","-C"])
rule="/srv/web10(/.*)?" in local and "httpd_sys_content_t" in "\n".join(x for x in local.splitlines() if "/srv/web10" in x)
checks=[
 {"label":"regra persistente de fcontext existe","pass":rule,"hint":"Use semanage fcontext -a."},
 {"label":"diretório está com httpd_sys_content_t","pass":"httpd_sys_content_t" in d,"hint":"Use restorecon."},
 {"label":"arquivo está com httpd_sys_content_t","pass":"httpd_sys_content_t" in f,"hint":"Aplique restorecon recursivamente."},
 {"label":"evidências foram salvas","pass":"httpd_sys_content_t" in read("contexts.txt") and "/srv/web10" in read("fcontext.txt"),"hint":"Salve contexts.txt e fcontext.txt."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj10-03","checks":checks,"score":score},ensure_ascii=False))
"""
def main():
 p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
 r=json_from_remote_python("servera",REMOTE_CHECKER); print(json.dumps(r,ensure_ascii=False)); return 0 if r["score"]==100 else 1
if __name__=="__main__": raise SystemExit(main())
