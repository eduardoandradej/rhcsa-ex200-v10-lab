#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
import json,subprocess
def run(a):
 p=subprocess.run(a,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 return p.returncode,p.stdout.strip()
_,pv=run(["sudo","-n","pvs","--noheadings","-o","pv_name,vg_name"])
_,vg=run(["sudo","-n","vgs","rhcsa_vgdata","--noheadings","--units","b","-o","vg_size"])
_,lv=run(["sudo","-n","lvs","rhcsa_vgdata/rhcsa_lvdata","--noheadings","--units","b","-o","lv_size"])
_,fst=run(["lsblk","-no","FSTYPE","/dev/rhcsa_vgdata/rhcsa_lvdata"])
try: size=int(float(lv.strip().rstrip("B")))
except: size=0
checks=[
 {"label":"PV pertence ao VG correto","pass":"/dev/vdc1" in pv and "rhcsa_vgdata" in pv,"hint":"Crie pvcreate e vgcreate."},
 {"label":"VG existe","pass":bool(vg.strip()),"hint":"Crie rhcsa_vgdata."},
 {"label":"LV tem aproximadamente 1536 MiB","pass":1450*1024**2 <= size <= 1600*1024**2,"hint":"Crie rhcsa_lvdata com 1536M."},
 {"label":"LV ainda não tem filesystem","pass":fst.strip()=="","hint":"Não execute mkfs neste lab."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj08-07","checks":checks,"score":score},ensure_ascii=False))
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
