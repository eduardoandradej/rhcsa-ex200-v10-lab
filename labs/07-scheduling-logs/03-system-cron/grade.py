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
cfg=scat("/etc/cron.d/rhcsa-report"); out=Path("/home/student/rhcsa-lab/obj07-03/output/cron.txt"); _,ac=run(["systemctl","is-active","crond"])
line=bool(re.search(r"(?m)^\*/5\s+\*\s+\*\s+\*\s+\*\s+student\s+/usr/bin/id\s+-un\s+>>\s+/home/student/rhcsa-lab/obj07-03/cron-run\.txt\s*$",cfg))
checks=[
 {"label":"arquivo em /etc/cron.d","pass":bool(cfg),"hint":"Crie rhcsa-report."},
 {"label":"schedule e usuário corretos","pass":line,"hint":"Use */5 e student."},
 {"label":"ambiente cron correto","pass":"SHELL=/bin/bash" in cfg and "PATH=/sbin:/bin:/usr/sbin:/usr/bin" in cfg and "MAILTO=root" in cfg,"hint":"Defina SHELL/PATH/MAILTO."},
 {"label":"crond ativo e evidência salva","pass":ac=="active" and out.is_file() and "student" in out.read_text(errors="replace"),"hint":"Salve cron.txt."}]
score=round(sum(c["pass"] for c in checks)/len(checks)*100); print(json.dumps({"lab_id":"obj07-03","checks":checks,"score":score},ensure_ascii=False))
"""
def main():
    p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
    result=json_from_remote_python("servera",REMOTE_CHECKER)
    print(json.dumps(result,ensure_ascii=False))
    return 0 if result["score"]==100 else 1
if __name__ == "__main__": raise SystemExit(main())
