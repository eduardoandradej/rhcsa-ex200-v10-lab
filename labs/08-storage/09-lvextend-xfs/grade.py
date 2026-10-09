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
_,lv=run(["sudo","-n","lvs","rhcsa_vgdata/rhcsa_lvdata","--noheadings","--units","b","-o","lv_size"])
_,fs=run(["df","-B1","--output=size","/lvextend"])
try: lvb=int(float(lv.strip().rstrip("B")))
except: lvb=0
try: fsb=int(fs.splitlines()[-1].strip())
except: fsb=0
keep=Path("/lvextend/keep.txt")
checks=[
 {"label":"LV foi estendido para cerca de 2 GiB","pass":1.9*1024**3 <= lvb <= 2.1*1024**3,"hint":"Use lvextend para tamanho total de 2G."},
 {"label":"XFS cresceu junto com o LV","pass":fsb >= 1.8*1024**3,"hint":"Use xfs_growfs /lvextend."},
 {"label":"dados anteriores foram preservados","pass":keep.is_file() and "PRESERVE-ME" in keep.read_text(errors="replace"),"hint":"Não recrie o filesystem."},
 {"label":"filesystem continua montado como XFS","pass":"xfs" in run(["findmnt","-n","-o","FSTYPE","/lvextend"])[1],"hint":"Mantenha /lvextend montado."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj08-09","checks":checks,"score":score},ensure_ascii=False))
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
