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
cfg=scat("/etc/rsyslog.d/rhcsa-debug.conf"); log=scat("/var/log/rhcsa-debug.log"); out=Path("/home/student/rhcsa-lab/obj07-04/output/log.txt"); _,ac=run(["systemctl","is-active","rsyslog"])
checks=[
 {"label":"regra rsyslog criada","pass":"local6.debug" in cfg and "/var/log/rhcsa-debug.log" in cfg,"hint":"Crie a regra."},
 {"label":"rsyslog ativo","pass":ac=="active","hint":"Reinicie rsyslog."},
 {"label":"mensagem no arquivo","pass":"OBJ07-RSYSLOG-DEBUG" in log,"hint":"Use logger."},
 {"label":"evidência salva","pass":out.is_file() and "OBJ07-RSYSLOG-DEBUG" in out.read_text(errors="replace"),"hint":"Salve log.txt."}]
score=round(sum(c["pass"] for c in checks)/len(checks)*100); print(json.dumps({"lab_id":"obj07-04","checks":checks,"score":score},ensure_ascii=False))
"""
def main():
    p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
    result=json_from_remote_python("servera",REMOTE_CHECKER)
    print(json.dumps(result,ensure_ascii=False))
    return 0 if result["score"]==100 else 1
if __name__ == "__main__": raise SystemExit(main())
