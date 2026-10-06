#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python
REMOTE_CHECKER = r"""
from pathlib import Path
import json,subprocess
def run(a):
 p=subprocess.run(a,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE); return p.returncode,p.stdout.strip()
_,tz=run(["timedatectl","show","-p","Timezone","--value"]); _,ac=run(["systemctl","is-active","chronyd"]); _,en=run(["systemctl","is-enabled","chronyd"])
r=Path("/home/student/rhcsa-lab/obj07-07/output")
def t(n):
 p=r/n; return p.read_text(errors="replace") if p.is_file() else ""
checks=[
 {"label":"fuso America/Jamaica","pass":tz=="America/Jamaica","hint":"Use set-timezone."},
 {"label":"chronyd ativo/habilitado","pass":ac=="active" and en=="enabled","hint":"Habilite NTP/chronyd."},
 {"label":"timedatectl registrado","pass":"America/Jamaica" in t("timedatectl.txt") and "NTP service:" in t("timedatectl.txt"),"hint":"Salve timedatectl."},
 {"label":"chronyc registrado","pass":"MS Name/IP address" in t("sources.txt") and "Reference ID" in t("tracking.txt"),"hint":"Salve sources/tracking."}]
score=round(sum(c["pass"] for c in checks)/len(checks)*100); print(json.dumps({"lab_id":"obj07-07","checks":checks,"score":score},ensure_ascii=False))
"""
def main():
    p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
    result=json_from_remote_python("servera",REMOTE_CHECKER)
    print(json.dumps(result,ensure_ascii=False))
    return 0 if result["score"]==100 else 1
if __name__ == "__main__": raise SystemExit(main())
