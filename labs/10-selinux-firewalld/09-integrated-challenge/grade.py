#!/usr/bin/env python3
import argparse,json,re
from labctl.remote import json_from_remote_python
REMOTE_CHECKER=r"""
from pathlib import Path
import subprocess,json,re
root=Path("/home/student/rhcsa-lab/obj10-09/output")
def run(args):
 p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE); return p.returncode,p.stdout.strip()
def read(n):
 p=root/n; return p.read_text(errors="replace").strip() if p.is_file() else ""
_,mode=run(["getenforce"])
_,ctx=run(["ls","-Zd","/srv/rhcsa10-final"])
_,fctx=run(["ls","-Z","/srv/rhcsa10-final/index.html"])
_,fcontext=run(["sudo","-n","semanage","fcontext","-l","-C"])
_,ports=run(["sudo","-n","semanage","port","-l","-C"])
_,iface=run(["bash","-lc","ip -o route show default | awk '{print $5; exit}'"])
_,zone=run(["sudo","-n","firewall-cmd",f"--get-zone-of-interface={iface}"])
if not zone or zone=="no zone":
 _,zone=run(["sudo","-n","firewall-cmd","--get-default-zone"])
fw_rc,fw=run(["sudo","-n","firewall-cmd",f"--zone={zone}","--query-port=48889/tcp"])
pfw_rc,pfw=run(["sudo","-n","firewall-cmd","--permanent",f"--zone={zone}","--query-port=48889/tcp"])
svc_rc,_=run(["systemctl","is-active","--quiet","httpd"])
curl_rc,curl=run(["curl","-sS","http://127.0.0.1:48889/secure10/index.html"])
port_ok=any("http_port_t" in x and "tcp" in x and re.search(r"(^|[ ,])48889([ ,]|$)",x) for x in ports.splitlines())
checks=[
 {"label":"SELinux permanece enforcing","pass":mode=="Enforcing","hint":"Não use permissive."},
 {"label":"fcontext persistente está correto","pass":"/srv/rhcsa10-final" in fcontext and "httpd_sys_content_t" in "\n".join(x for x in fcontext.splitlines() if "/srv/rhcsa10-final" in x),"hint":"Use semanage fcontext."},
 {"label":"conteúdo está corretamente rotulado","pass":"httpd_sys_content_t" in ctx and "httpd_sys_content_t" in fctx,"hint":"Use restorecon."},
 {"label":"48889/tcp está rotulada http_port_t","pass":port_ok,"hint":"Use semanage port."},
 {"label":"firewall runtime e permanente permitem 48889/tcp","pass":fw_rc==0 and fw=="yes" and pfw_rc==0 and pfw=="yes","hint":"Use --permanent e --reload na zona correta."},
 {"label":"httpd está ativo","pass":svc_rc==0,"hint":"Inicie o serviço após corrigir SELinux."},
 {"label":"aplicação responde localmente","pass":curl_rc==0 and curl.strip()=="OBJ10 integrated security PASS","hint":"Valide com curl."},
 {"label":"evidências foram salvas","pass":"httpd_sys_content_t" in read("contexts.txt") and "48889" in read("selinux-port.txt") and read("zone.txt")==zone and read("firewall.txt")=="yes" and "OBJ10 integrated security PASS" in read("curl.txt"),"hint":"Salve todos os arquivos solicitados."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj10-09","checks":checks,"score":score},ensure_ascii=False))
"""
def main():
 p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
 r=json_from_remote_python("servera",REMOTE_CHECKER); print(json.dumps(r,ensure_ascii=False)); return 0 if r["score"]==100 else 1
if __name__=="__main__": raise SystemExit(main())
