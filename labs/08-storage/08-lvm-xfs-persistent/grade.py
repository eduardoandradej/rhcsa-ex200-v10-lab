#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json,subprocess,re
dev="/dev/rhcsa_vgdata/rhcsa_lvdata"
def run(a):
 p=subprocess.run(a,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 return p.returncode,p.stdout.strip()
_,typ=run(["sudo","-n","blkid","-s","TYPE","-o","value",dev])
_,label=run(["sudo","-n","blkid","-s","LABEL","-o","value",dev])
_,uuid=run(["sudo","-n","blkid","-s","UUID","-o","value",dev])
_,mnt=run(["findmnt","-n","-o","SOURCE,FSTYPE","/lvdata"])
_,fstab=run(["sudo","-n","cat","/etc/fstab"])
rc,_=run(["findmnt","--verify","--tab-file","/etc/fstab"])
lines=[l for l in fstab.splitlines() if l.strip() and not l.lstrip().startswith("#")]
match=any(re.search(rf"^UUID={re.escape(uuid)}\s+/lvdata\s+xfs\s+defaults\s+0\s+0$",l) for l in lines)
marker=Path("/lvdata/marker.txt")
checks=[
 {"label":"LV contém XFS com label correto","pass":typ=="xfs" and label=="LVDATA08","hint":"Use mkfs.xfs -L LVDATA08."},
 {"label":"mount persistente usa UUID","pass":match and "xfs" in mnt,"hint":"Use UUID no fstab e mount /lvdata."},
 {"label":"marker existe no LV","pass":marker.is_file() and "OBJ08-LVDATA" in marker.read_text(errors="replace"),"hint":"Crie marker.txt."},
 {"label":"fstab é válido","pass":rc==0,"hint":"Use findmnt --verify."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj08-08","checks":checks,"score":score},ensure_ascii=False))
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
