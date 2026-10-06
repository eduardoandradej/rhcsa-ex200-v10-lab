#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python
REMOTE_CHECKER = r"""
from pathlib import Path
import json,subprocess
def run(a):
 p=subprocess.run(a,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE); return p.returncode,p.stdout.strip()
def scat(p):
 rc,out=run(["sudo","-n","cat",p]); return out if rc==0 else ""
svc=scat("/etc/systemd/system/rhcsa-audit.service"); timer=scat("/etc/systemd/system/rhcsa-audit.timer"); rule=scat("/etc/rsyslog.d/rhcsa-audit.conf"); log=scat("/var/log/rhcsa-audit.log")
_,ac=run(["systemctl","is-active","rhcsa-audit.timer"]); _,en=run(["systemctl","is-enabled","rhcsa-audit.timer"])
r=Path("/home/student/rhcsa-lab/obj07-08/output")
def t(n):
 p=r/n; return p.read_text(errors="replace") if p.is_file() else ""
checks=[
 {"label":"regra rsyslog correta","pass":"local5.notice" in rule and "/var/log/rhcsa-audit.log" in rule,"hint":"Configure a regra."},
 {"label":"serviço oneshot correto","pass":"Type=oneshot" in svc and "local5.notice" in svc and "OBJ07-INTEGRATED-AUDIT" in svc,"hint":"Crie o serviço."},
 {"label":"timer correto","pass":"OnBootSec=1min" in timer and "OnUnitActiveSec=5min" in timer,"hint":"Configure o timer."},
 {"label":"timer ativo/habilitado","pass":ac=="active" and en=="enabled","hint":"Use enable --now."},
 {"label":"syslog contém evidência","pass":"OBJ07-INTEGRATED-AUDIT" in log and "OBJ07-INTEGRATED-AUDIT" in t("syslog.txt"),"hint":"Inicie o serviço e salve o log."},
 {"label":"journal contém evidência","pass":"OBJ07-INTEGRATED-AUDIT" in t("journal.txt"),"hint":"Filtre por tag."},
 {"label":"timer evidence salvo","pass":"rhcsa-audit.timer" in t("timer.txt"),"hint":"Salve status do timer."}]
score=round(sum(c["pass"] for c in checks)/len(checks)*100); print(json.dumps({"lab_id":"obj07-08","checks":checks,"score":score},ensure_ascii=False))
"""
def main():
    p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
    result=json_from_remote_python("serverb",REMOTE_CHECKER)
    print(json.dumps(result,ensure_ascii=False))
    return 0 if result["score"]==100 else 1
if __name__ == "__main__": raise SystemExit(main())
