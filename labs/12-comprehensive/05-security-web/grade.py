#!/usr/bin/env python3
import argparse,json,re,subprocess
from pathlib import Path
from labctl.remote import json_from_remote_python

REMOTE_CHECKER=r"""
from pathlib import Path
import subprocess,json,re
root=Path("/home/student/rhcsa-lab/obj12-05/output")
def run(args):
    p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return p.returncode,p.stdout.strip()
def read(n):
    p=root/n
    return p.read_text(errors="replace").strip() if p.is_file() else ""

_,mode=run(["getenforce"])
_,ctx=run(["ls","-Zd","/srv/secure12"])
_,fctx=run(["ls","-Z","/srv/secure12/index.html"])
_,rules=run(["sudo","-n","semanage","fcontext","-l","-C"])
_,ports=run(["sudo","-n","semanage","port","-l","-C"])

_,iface=run(["bash","-lc","ip -o route show default | awk '{print $5; exit}'"])
_,zone=run(["sudo","-n","firewall-cmd",f"--get-zone-of-interface={iface}"])
if not zone or zone=="no zone":
    _,zone=run(["sudo","-n","firewall-cmd","--get-default-zone"])
fw_rc,fw=run(["sudo","-n","firewall-cmd",f"--zone={zone}","--query-port=48890/tcp"])
pfw_rc,pfw=run(["sudo","-n","firewall-cmd","--permanent",f"--zone={zone}","--query-port=48890/tcp"])

act,_=run(["systemctl","is-active","--quiet","httpd"])
ena,_=run(["systemctl","is-enabled","--quiet","httpd"])
curl_rc,curl=run(["curl","-sS","http://127.0.0.1:48890/secure12/index.html"])

port_ok=any("http_port_t" in x and "tcp" in x and re.search(r"(^|[ ,])48890([ ,]|$)",x) for x in ports.splitlines())

checks=[
 {"label":"SELinux permanece enforcing","pass":mode=="Enforcing","hint":"Não use permissive."},
 {"label":"contexto persistente e aplicado está correto","pass":"/srv/secure12" in rules and "httpd_sys_content_t" in "\n".join(x for x in rules.splitlines() if "/srv/secure12" in x) and "httpd_sys_content_t" in ctx and "httpd_sys_content_t" in fctx,"hint":"Use semanage fcontext e restorecon."},
 {"label":"48890/tcp está rotulada http_port_t","pass":port_ok,"hint":"Use semanage port."},
 {"label":"firewall runtime e permanente permitem 48890/tcp","pass":fw_rc==0 and fw=="yes" and pfw_rc==0 and pfw=="yes","hint":"Abra a porta permanentemente e recarregue."},
 {"label":"httpd está ativo e habilitado","pass":act==0 and ena==0,"hint":"Use systemctl enable --now httpd."},
 {"label":"serviço responde corretamente","pass":curl_rc==0 and curl=="OBJ12 secure service ready","hint":"Valide a página com curl."},
 {"label":"evidências foram salvas","pass":"httpd_sys_content_t" in read("contexts.txt") and "48890" in read("selinux-port.txt") and read("firewall.txt")=="yes" and "active" in read("service.txt") and "enabled" in read("service.txt") and read("curl.txt")=="OBJ12 secure service ready","hint":"Salve as cinco evidências pedidas."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj12-05","checks":checks,"score":score},ensure_ascii=False))
"""

def main():
    p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
    r=json_from_remote_python("servera",REMOTE_CHECKER)
    print(json.dumps(r,ensure_ascii=False))
    return 0 if r["score"]==100 else 1
if __name__=="__main__":
    raise SystemExit(main())
