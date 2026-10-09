#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
import json,subprocess
def run(a):
 p=subprocess.run(a,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 return p.returncode,p.stdout.strip()
_,pvs=run(["sudo","-n","pvs","--noheadings","-o","pv_name,vg_name"])
_,npv=run(["sudo","-n","vgs","rhcsa_vgextend","--noheadings","-o","pv_count"])
_,lv=run(["sudo","-n","lvs","rhcsa_vgextend/rhcsa_lvextra","--noheadings","--units","b","-o","lv_size"])
try: size=int(float(lv.strip().rstrip("B")))
except: size=0
checks=[
 {"label":"VG possui dois PVs","pass":npv.strip()=="2" and "/dev/vdc1" in pvs and "/dev/vdd1" in pvs,"hint":"Use pvcreate e vgextend."},
 {"label":"ambos PVs pertencem ao VG correto","pass":pvs.count("rhcsa_vgextend")>=2,"hint":"Confira pvs."},
 {"label":"LV extra de 2 GiB foi criado","pass":1.9*1024**3 <= size <= 2.1*1024**3,"hint":"Crie rhcsa_lvextra com 2G."},
 {"label":"disco de sistema não entrou no VG","pass":"/dev/vda" not in "\n".join(l for l in pvs.splitlines() if "rhcsa_vgextend" in l),"hint":"Nunca use /dev/vda."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj08-10","checks":checks,"score":score},ensure_ascii=False))
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
