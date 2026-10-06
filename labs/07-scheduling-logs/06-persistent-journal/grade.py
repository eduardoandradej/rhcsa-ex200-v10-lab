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
cfg=scat("/etc/systemd/journald.conf.d/99-rhcsa-persistent.conf"); _,ac=run(["systemctl","is-active","systemd-journald"]); _,files=run(["sudo","-n","find","/var/log/journal","-type","f","-name","*.journal","-print"])
r=Path("/home/student/rhcsa-lab/obj07-06/output")
def t(n):
 p=r/n; return p.read_text(errors="replace") if p.is_file() else ""
checks=[
 {"label":"drop-in persistente correto","pass":"Storage=persistent" in cfg and "SystemMaxUse=100M" in cfg,"hint":"Crie o drop-in."},
 {"label":"journald ativo","pass":ac=="active","hint":"Reinicie journald."},
 {"label":"arquivos persistentes existem","pass":bool(files.strip()),"hint":"Crie /var/log/journal e flush."},
 {"label":"evidências salvas","pass":bool(t("boots.txt").strip()) and "journals take up" in t("disk-usage.txt"),"hint":"Salve boots/disk usage."}]
score=round(sum(c["pass"] for c in checks)/len(checks)*100); print(json.dumps({"lab_id":"obj07-06","checks":checks,"score":score},ensure_ascii=False))
"""
def main():
    p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
    result=json_from_remote_python("servera",REMOTE_CHECKER)
    print(json.dumps(result,ensure_ascii=False))
    return 0 if result["score"]==100 else 1
if __name__ == "__main__": raise SystemExit(main())
