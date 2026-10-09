#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json,subprocess
def run(a):
 p=subprocess.run(a,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 return p.returncode,p.stdout.strip()
_,fst=run(["lsblk","-no","FSTYPE","/dev/vdb1"])
_,label=run(["sudo","-n","blkid","-s","LABEL","-o","value","/dev/vdb1"])
_,src=run(["findmnt","-n","-o","SOURCE,FSTYPE","/mnt/rhcsa-xfs"])
marker=Path("/mnt/rhcsa-xfs/obj08.txt")
fstab=run(["sudo","-n","cat","/etc/fstab"])[1]
checks=[
 {"label":"filesystem XFS correto","pass":fst=="xfs" and label=="RHCSA08XFS","hint":"Use mkfs.xfs com label."},
 {"label":"mount temporário correto","pass":"/dev/vdb1" in src and "xfs" in src,"hint":"Monte vdb1 em /mnt/rhcsa-xfs."},
 {"label":"arquivo de teste persiste no XFS","pass":marker.is_file() and "OBJ08-XFS" in marker.read_text(errors="replace"),"hint":"Crie obj08.txt no filesystem montado."},
 {"label":"fstab não foi alterado para este mount","pass":"/mnt/rhcsa-xfs" not in fstab,"hint":"Este lab pede mount temporário."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj08-03","checks":checks,"score":score},ensure_ascii=False))
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
