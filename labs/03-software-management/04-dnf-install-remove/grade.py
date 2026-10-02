#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
import json, subprocess
def q(name):
    p=subprocess.run(["rpm","-q","--qf","%{VERSION}-%{RELEASE}\n",name],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return p.returncode,p.stdout.strip()

rc_tool,ver_tool=q("rhcsa-toolkit")
rc_temp,_=q("rhcsa-temp")
checks=[
 {"label":"rhcsa-toolkit está instalado","pass":rc_tool==0,"hint":"Use dnf install rhcsa-toolkit."},
 {"label":"rhcsa-toolkit está na versão 1.0-1","pass":ver_tool=="1.0-1","hint":"Verifique a versão instalada com rpm -q."},
 {"label":"rhcsa-temp foi removido","pass":rc_temp!=0,"hint":"Use dnf remove rhcsa-temp."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj03-04","checks":checks,"score":score},ensure_ascii=False))
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.parse_args()

    payload = json_from_remote_python("servera", REMOTE_CHECKER)
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload["score"] == 100 else 1

if __name__ == "__main__":
    raise SystemExit(main())
