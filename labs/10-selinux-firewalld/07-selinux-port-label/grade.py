#!/usr/bin/env python3
import argparse,json,re
from labctl.remote import json_from_remote_python
REMOTE_CHECKER=r"""
from pathlib import Path
import subprocess,json,re
root=Path("/home/student/rhcsa-lab/obj10-07/output")
def run(args):
 p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE); return p.returncode,p.stdout.strip()
_,mode=run(["getenforce"])
_,ports=run(["sudo","-n","semanage","port","-l","-C"])
svc_rc,_=run(["systemctl","is-active","--quiet","httpd"])
_,ss=run(["sudo","-n","ss","-ltnp"])
custom=any("http_port_t" in x and "tcp" in x and re.search(r"(^|[ ,])48888([ ,]|$)",x) for x in ports.splitlines())
checks=[
 {"label":"SELinux permanece enforcing","pass":mode=="Enforcing","hint":"Mantenha enforcing."},
 {"label":"48888/tcp está rotulada http_port_t","pass":custom,"hint":"Use semanage port -a -t http_port_t -p tcp 48888."},
 {"label":"httpd está ativo","pass":svc_rc==0,"hint":"Inicie httpd depois de corrigir a porta."},
 {"label":"httpd está escutando em 48888","pass":":48888" in ss,"hint":"Verifique com ss."},
 {"label":"evidências foram salvas","pass":"48888" in ((root/"ports.txt").read_text(errors="replace") if (root/"ports.txt").is_file() else "") and "48888" in ((root/"listen.txt").read_text(errors="replace") if (root/"listen.txt").is_file() else ""),"hint":"Salve ports.txt e listen.txt."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj10-07","checks":checks,"score":score},ensure_ascii=False))
"""
def main():
 p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
 r=json_from_remote_python("servera",REMOTE_CHECKER); print(json.dumps(r,ensure_ascii=False)); return 0 if r["score"]==100 else 1
if __name__=="__main__": raise SystemExit(main())
