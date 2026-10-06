#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python
REMOTE_CHECKER = r"""
from pathlib import Path
import json,subprocess,re
def run(a):
 p=subprocess.run(a,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE); return p.returncode,p.stdout.strip()
def scat(p):
 rc,out=run(["sudo","-n","cat",p]); return out if rc==0 else ""
cfg=scat("/etc/systemd/system/sysstat-collect.timer")
_,en=run(["systemctl","is-enabled","sysstat-collect.timer"]); _,ac=run(["systemctl","is-active","sysstat-collect.timer"])
r=Path("/home/student/rhcsa-lab/obj07-01/output")
def t(n):
 p=r/n; return p.read_text(errors="replace") if p.is_file() else ""
checks=[
 {"label":"override em /etc/systemd/system","pass":bool(cfg),"hint":"Copie o timer para /etc/systemd/system."},
 {"label":"timer configurado para 2 minutos","pass":bool(re.search(r"(?m)^OnCalendar=.*(?:00/2|/2)",cfg)),"hint":"Ajuste OnCalendar."},
 {"label":"timer habilitado e ativo","pass":en=="enabled" and ac=="active","hint":"Use enable --now."},
 {"label":"evidências salvas","pass":"OnCalendar" in t("timer.txt") and "sysstat-collect.timer" in t("list-timers.txt"),"hint":"Salve cat/list-timers."}]
score=round(sum(c["pass"] for c in checks)/len(checks)*100); print(json.dumps({"lab_id":"obj07-01","checks":checks,"score":score},ensure_ascii=False))
"""
def main():
    p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
    result=json_from_remote_python("servera",REMOTE_CHECKER)
    print(json.dumps(result,ensure_ascii=False))
    return 0 if result["score"]==100 else 1
if __name__ == "__main__": raise SystemExit(main())
