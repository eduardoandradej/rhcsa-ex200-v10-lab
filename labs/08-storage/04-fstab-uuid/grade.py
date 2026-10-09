#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
import json,subprocess,re
def run(a):
 p=subprocess.run(a,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 return p.returncode,p.stdout.strip()
_,uuid=run(["sudo","-n","blkid","-s","UUID","-o","value","/dev/vdb1"])
_,fstab=run(["sudo","-n","cat","/etc/fstab"])
_,mnt=run(["findmnt","-n","-o","SOURCE,FSTYPE,OPTIONS","/data1"])
rc_verify,_=run(["findmnt","--verify","--tab-file","/etc/fstab"])
lines=[l for l in fstab.splitlines() if l.strip() and not l.lstrip().startswith("#")]
match=any(re.search(rf"^UUID={re.escape(uuid)}\s+/data1\s+xfs\s+defaults\s+0\s+0\s*$",l) for l in lines)
checks=[
 {"label":"fstab usa UUID correto","pass":bool(uuid) and match,"hint":"Use UUID=<uuid> /data1 xfs defaults 0 0."},
 {"label":"fstab não usa caminho volátil do device","pass":not any("/dev/vdb1" in l and "/data1" in l for l in lines),"hint":"Use UUID em vez de /dev/vdb1."},
 {"label":"filesystem está montado em /data1","pass":"xfs" in mnt and bool(mnt),"hint":"Use mount /data1."},
 {"label":"fstab passa na verificação","pass":rc_verify==0,"hint":"Corrija findmnt --verify antes de finalizar."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj08-04","checks":checks,"score":score},ensure_ascii=False))
"""

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--json", action="store_true")
    p.parse_args()
    result = json_from_remote_python("servera", REMOTE_CHECKER)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["score"] == 100 else 1

if __name__ == "__main__":
    raise SystemExit(main())
