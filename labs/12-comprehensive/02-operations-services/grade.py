#!/usr/bin/env python3
import argparse, json, os, stat, subprocess
from pathlib import Path
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import subprocess, json, stat, pwd, grp

root=Path("/home/student/rhcsa-lab/obj12-02/output")
def run(args):
    p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return p.returncode,p.stdout.strip()
def read(n):
    p=root/n
    return p.read_text(errors="replace").strip() if p.is_file() else ""

act,_=run(["systemctl","is-active","--quiet","httpd"])
ena,_=run(["systemctl","is-enabled","--quiet","httpd"])
curl_rc,curl=run(["curl","-sS","http://127.0.0.1/ops12.html"])

cron=Path("/etc/cron.d/ops12").read_text(errors="replace").strip() if Path("/etc/cron.d/ops12").is_file() else ""
tmp=Path("/run/ops12")
tmp_ok=False
if tmp.is_dir():
    st=tmp.stat()
    tmp_ok=(stat.S_IMODE(st.st_mode)==0o750 and pwd.getpwuid(st.st_uid).pw_name=="student" and grp.getgrgid(st.st_gid).gr_name=="student")

rsconf=Path("/etc/rsyslog.d/ops12.conf").read_text(errors="replace") if Path("/etc/rsyslog.d/ops12.conf").is_file() else ""
log_rc,log=run(["sudo","-n","cat","/var/log/ops12.log"])
if log_rc != 0:
    log = ""

checks=[
 {"label":"httpd está ativo e habilitado","pass":act==0 and ena==0,"hint":"Use systemctl enable --now httpd."},
 {"label":"página operacional responde","pass":curl_rc==0 and curl=="OBJ12 operations ready","hint":"Crie ops12.html e valide com curl."},
 {"label":"cron está configurado a cada 10 minutos como student","pass":"*/10 * * * * student /usr/bin/date >> /home/student/ops12-cron.log" in cron,"hint":"Corrija /etc/cron.d/ops12."},
 {"label":"tmpfiles criou /run/ops12 corretamente","pass":tmp_ok,"hint":"Use modo 0750 e student:student."},
 {"label":"rsyslog roteia local6 e recebeu a mensagem","pass":"local6.*" in rsconf and "/var/log/ops12.log" in rsconf and "OBJ12 operations ready" in log,"hint":"Configure rsyslog, reinicie e envie com logger."},
 {"label":"evidências foram salvas","pass":read("curl.txt")=="OBJ12 operations ready" and "active" in read("httpd.txt") and "enabled" in read("httpd.txt") and "*/10" in read("cron.txt") and "750 student student" in read("tmpfiles.txt") and "OBJ12 operations ready" in read("log.txt"),"hint":"Salve as cinco evidências pedidas."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj12-02","checks":checks,"score":score},ensure_ascii=False))
"""

def main():
    p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
    r=json_from_remote_python("servera",REMOTE_CHECKER)
    print(json.dumps(r,ensure_ascii=False))
    return 0 if r["score"]==100 else 1
if __name__=="__main__":
    raise SystemExit(main())
