#!/usr/bin/env python3
import argparse,json,os,pwd,grp,stat,subprocess
from pathlib import Path
from labctl.remote import json_from_remote_python

REMOTE_CHECKER=r"""
from pathlib import Path
import subprocess,json,os,pwd,grp,stat

root=Path("/home/student/rhcsa-lab/obj12-06/output")
def run(args):
    p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return p.returncode,p.stdout.strip()
def read(n):
    p=root/n
    return p.read_text(errors="replace").strip() if p.is_file() else ""

try:
    pw=pwd.getpwnam("operator12")
    groups=[g.gr_name for g in grp.getgrall() if "operator12" in g.gr_mem]
    user_ok=pw.pw_shell=="/bin/bash" and "opsfinal12" in groups
except KeyError:
    user_ok=False

try:
    gid=grp.getgrnam("opsfinal12").gr_gid
except KeyError:
    gid=-1
d=Path("/srv/final12")
dir_ok=False
if d.is_dir():
    st=d.stat()
    dir_ok=st.st_uid==0 and st.st_gid==gid and stat.S_IMODE(st.st_mode)==0o2770

master=Path("/etc/auto.master.d/final12.autofs").read_text(errors="replace") if Path("/etc/auto.master.d/final12.autofs").is_file() else ""
mapf=Path("/etc/auto.final12").read_text(errors="replace") if Path("/etc/auto.final12").is_file() else ""
act,_=run(["systemctl","is-active","--quiet","autofs"])
ena,_=run(["systemctl","is-enabled","--quiet","autofs"])

script=Path("/usr/local/bin/final-report12")
script_ok=script.is_file() and os.access(script,os.X_OK)
test_red,_=run(["sudo","-n","-u","operator12","/usr/local/bin/final-report12","red"]) if script_ok else (1,"")
test_hat,_=run(["sudo","-n","-u","operator12","/usr/local/bin/final-report12","hat"]) if script_ok else (1,"")
red_rc,red=run(["sudo","-n","cat","/srv/final12/report-red.txt"])
hat_rc,hat=run(["sudo","-n","cat","/srv/final12/report-hat.txt"])
if red_rc != 0:
    red = ""
if hat_rc != 0:
    hat = ""
cron=Path("/etc/cron.d/final12").read_text(errors="replace").strip() if Path("/etc/cron.d/final12").is_file() else ""

checks=[
 {"label":"usuário, grupo e diretório final estão corretos","pass":user_ok and dir_ok,"hint":"Configure operator12, opsfinal12 e /srv/final12."},
 {"label":"mapa AutoFS indireto está correto","pass":"/remote12-final /etc/auto.final12" in master and "*" in mapf and "serverb:/srv/rhcsa11/integrated/&" in mapf and "rw" in mapf and "sync" in mapf,"hint":"Configure o mapa wildcard indireto."},
 {"label":"autofs está ativo e habilitado","pass":act==0 and ena==0,"hint":"Use systemctl enable --now autofs."},
 {"label":"script funciona como operator12","pass":script_ok and test_red==0 and test_hat==0 and red=="OBJ11 RED team" and hat=="OBJ11 HAT team","hint":"O script deve ler red/hat e gravar os relatórios."},
 {"label":"cron executa o relatório red a cada 15 minutos","pass":"*/15 * * * * operator12 /usr/local/bin/final-report12 red" in cron,"hint":"Configure /etc/cron.d/final12."},
 {"label":"evidências finais foram salvas","pass":"operator12" in read("id.txt") and "serverb:/srv/rhcsa11/integrated/red" in read("mounts.txt") and "serverb:/srv/rhcsa11/integrated/hat" in read("mounts.txt") and "OBJ11 RED team" in read("reports.txt") and "OBJ11 HAT team" in read("reports.txt") and "*/15" in read("cron.txt"),"hint":"Salve id, mounts, reports e cron."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj12-06","checks":checks,"score":score},ensure_ascii=False))
"""

def main():
    p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
    r=json_from_remote_python("servera",REMOTE_CHECKER)
    print(json.dumps(r,ensure_ascii=False))
    return 0 if r["score"]==100 else 1
if __name__=="__main__":
    raise SystemExit(main())
