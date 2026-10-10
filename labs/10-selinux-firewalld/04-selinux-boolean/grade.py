#!/usr/bin/env python3
import argparse,json,re
from labctl.remote import json_from_remote_python
REMOTE_CHECKER=r"""
from pathlib import Path
import subprocess,json,re
root=Path("/home/student/rhcsa-lab/obj10-04/output")
def run(args):
 p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE); return p.returncode,p.stdout.strip()
def read(n):
 p=root/n; return p.read_text(errors="replace").strip() if p.is_file() else ""
_,cur=run(["getsebool","httpd_enable_homedirs"])
_,sem=run(["sudo","-n","semanage","boolean","-l"])
_,custom=run(["sudo","-n","semanage","boolean","-l","-C"])
line=next((x for x in sem.splitlines() if x.startswith("httpd_enable_homedirs ")), "")
persistent=bool(re.search(r"\(on\s*,\s*on\)",line))
checks=[
 {"label":"Boolean atual está on","pass":"--> on" in cur,"hint":"Use setsebool."},
 {"label":"Boolean persistente está on","pass":persistent,"hint":"Use setsebool -P."},
 {"label":"customização persistente está registrada","pass":"httpd_enable_homedirs" in custom,"hint":"Confirme com semanage boolean -l -C."},
 {"label":"evidências foram salvas","pass":"--> on" in read("getsebool.txt") and "httpd_enable_homedirs" in read("semanage.txt") and "httpd_enable_homedirs" in read("custom.txt"),"hint":"Salve os três arquivos pedidos."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj10-04","checks":checks,"score":score},ensure_ascii=False))
"""
def main():
 p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
 r=json_from_remote_python("servera",REMOTE_CHECKER); print(json.dumps(r,ensure_ascii=False)); return 0 if r["score"]==100 else 1
if __name__=="__main__": raise SystemExit(main())
