#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json,subprocess,re
data="/dev/rhcsa_vgfinal/rhcsa_data"; swapdev="/dev/rhcsa_vgfinal/rhcsa_swap"
def run(a):
 p=subprocess.run(a,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 return p.returncode,p.stdout.strip()

def active_swap_uuids():
    rc, names = run(["swapon", "--show=NAME", "--noheadings", "--raw"])
    if rc != 0:
        return set()
    uuids = set()
    for name in names.splitlines():
        name = name.strip()
        if not name:
            continue
        _, value = run(["sudo", "-n", "blkid", "-s", "UUID", "-o", "value", name])
        if value:
            uuids.add(value.strip())
    return uuids

def baseline_swap_uuids(lab_id):
    rc, out = run([
        "sudo", "-n", "cat",
        f"/var/lib/rhcsa-lab/{lab_id}/swap-uuids.before"
    ])
    if rc != 0:
        return set()
    return {x.strip() for x in out.splitlines() if x.strip()}

_,pvs=run(["sudo","-n","pvs","--noheadings","-o","pv_name,vg_name"])
_,npv=run(["sudo","-n","vgs","rhcsa_vgfinal","--noheadings","-o","pv_count"])
_,dlv=run(["sudo","-n","lvs","rhcsa_vgfinal/rhcsa_data","--noheadings","--units","b","-o","lv_size"])
_,slv=run(["sudo","-n","lvs","rhcsa_vgfinal/rhcsa_swap","--noheadings","--units","b","-o","lv_size"])
_,dtype=run(["sudo","-n","blkid","-s","TYPE","-o","value",data]); _,dlabel=run(["sudo","-n","blkid","-s","LABEL","-o","value",data]); _,duuid=run(["sudo","-n","blkid","-s","UUID","-o","value",data])
_,stype=run(["sudo","-n","blkid","-s","TYPE","-o","value",swapdev]); _,slabel=run(["sudo","-n","blkid","-s","LABEL","-o","value",swapdev]); _,suuid=run(["sudo","-n","blkid","-s","UUID","-o","value",swapdev])
_,fstab=run(["sudo","-n","cat","/etc/fstab"]); _,mnt=run(["findmnt","-n","-o","SOURCE,FSTYPE","/lvfinal"])
active=active_swap_uuids()
baseline=baseline_swap_uuids("obj08-12")
_,df=run(["df","-B1","--output=size","/lvfinal"]); rc,_=run(["findmnt","--verify","--tab-file","/etc/fstab"])
try: db=int(float(dlv.strip().rstrip("B")))
except: db=0
try: sb=int(float(slv.strip().rstrip("B")))
except: sb=0
try: fsb=int(df.splitlines()[-1].strip())
except: fsb=0
lines=[l for l in fstab.splitlines() if l.strip() and not l.lstrip().startswith("#")]
dline=any(re.search(rf"^UUID={re.escape(duuid)}\s+/lvfinal\s+xfs\s+defaults\s+0\s+0$",l) for l in lines)
sline=any(re.search(rf"^UUID={re.escape(suuid)}\s+none\s+swap\s+defaults\s+0\s+0$",l) for l in lines)
marker=Path("/lvfinal/marker.txt")
checks=[
 {"label":"VG final usa os dois PVs scratch","pass":npv.strip()=="2" and "/dev/vdc1" in pvs and "/dev/vdd1" in pvs and pvs.count("rhcsa_vgfinal")>=2,"hint":"Crie PVs em vdc1/vdd1 e um único VG."},
 {"label":"data LV foi estendido para 3 GiB","pass":2.9*1024**3 <= db <= 3.1*1024**3,"hint":"Estenda rhcsa_data para 3G."},
 {"label":"XFS cresceu e preservou dados","pass":dtype=="xfs" and dlabel=="FINAL08" and fsb>=2.7*1024**3 and marker.is_file() and "OBJ08-FINAL" in marker.read_text(errors="replace"),"hint":"Use xfs_growfs sem recriar o filesystem."},
 {"label":"mount persistente usa UUID","pass":dline and "xfs" in mnt,"hint":"Persistência de /lvfinal por UUID."},
 {"label":"swap LV correto e ativo por UUID","pass":450*1024**2 <= sb <= 600*1024**2 and stype=="swap" and slabel=="FINALSWAP08" and bool(suuid) and suuid in active,"hint":"Crie e ative o swap LV."},
 {"label":"swap persistente usa UUID","pass":sline,"hint":"Persista o swap por UUID."},
 {"label":"swap original permanece ativo","pass":bool(baseline) and baseline.issubset(active),"hint":"Preserve o swap original."},
 {"label":"fstab final é válido","pass":rc==0,"hint":"Use findmnt --verify."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj08-12","checks":checks,"score":score},ensure_ascii=False))
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
