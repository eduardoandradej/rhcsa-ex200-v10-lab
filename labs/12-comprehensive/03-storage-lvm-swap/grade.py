#!/usr/bin/env python3
import argparse, json, os, re, subprocess
from pathlib import Path
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import subprocess, json, os, re

root=Path("/home/student/rhcsa-lab/obj12-03/output")
def run(args):
    p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return p.returncode,p.stdout.strip(),p.stderr.strip()
def read(n):
    p=root/n
    return p.read_text(errors="replace").strip() if p.is_file() else ""

part_rc,parted,_=run(["sudo","-n","parted","-sm","/dev/vdb","unit","B","print"])
part_ok=False
if part_rc==0:
    lines=parted.splitlines()
    gpt=any(":gpt:" in x for x in lines)
    p1=next((x for x in lines if x.startswith("1:")), "")
    fields=p1.split(":")
    try:
        size=int(fields[3].rstrip("B"))
    except Exception:
        size=0
    part_ok=gpt and size >= 3*1024**3

pv_rc,pvs,_=run(["sudo","-n","pvs","--noheadings","-o","pv_name,vg_name"])
pv_ok=pv_rc==0 and "/dev/vdb1" in pvs and "vg12" in pvs

lv_rc,lvs,_=run(["sudo","-n","lvs","--noheadings","--units","m","--nosuffix","-o","lv_name,lv_size","vg12"])
sizes={}
if lv_rc==0:
    for line in lvs.splitlines():
        parts=line.split()
        if len(parts)>=2:
            try: sizes[parts[0]]=float(parts[1].replace("<","").replace(">",""))
            except Exception: pass

data_dev="/dev/vg12/lvdata"
swap_dev="/dev/vg12/lvswap"
_,data_uuid,_=run(["sudo","-n","blkid","-s","UUID","-o","value",data_dev])
_,data_label,_=run(["sudo","-n","blkid","-s","LABEL","-o","value",data_dev])
_,data_type,_=run(["sudo","-n","blkid","-s","TYPE","-o","value",data_dev])
_,swap_uuid,_=run(["sudo","-n","blkid","-s","UUID","-o","value",swap_dev])
_,swap_label,_=run(["sudo","-n","blkid","-s","LABEL","-o","value",swap_dev])
_,swap_type,_=run(["sudo","-n","blkid","-s","TYPE","-o","value",swap_dev])

fm_rc,fm,_=run(["findmnt","-n","-o","SOURCE,FSTYPE,TARGET","/srv/data12"])
verify_rc,_,_=run(["sudo","-n","findmnt","--verify"])

fstab=Path("/etc/fstab").read_text(errors="replace")
data_fstab=bool(data_uuid and re.search(rf"(?m)^UUID={re.escape(data_uuid)}\s+/srv/data12\s+xfs\s+defaults\s+0\s+0\s*$",fstab))
swap_fstab=bool(swap_uuid and re.search(rf"(?m)^UUID={re.escape(swap_uuid)}\s+none\s+swap\s+defaults\s+0\s+0\s*$",fstab))

swap_active=False
target=os.path.realpath(swap_dev)
try:
    for line in Path("/proc/swaps").read_text().splitlines()[1:]:
        fields=line.split()
        if fields and os.path.realpath(fields[0]) == target:
            swap_active=True
            break
except Exception:
    pass

checks=[
 {"label":"GPT e partição de pelo menos 3 GiB existem em vdb","pass":part_ok,"hint":"Use somente /dev/vdb e crie GPT + /dev/vdb1."},
 {"label":"PV e VG vg12 estão corretos","pass":pv_ok,"hint":"Crie o PV em /dev/vdb1 e o VG vg12."},
 {"label":"lvdata tem tamanho, XFS e label corretos","pass":sizes.get("lvdata",0)>=1400 and data_type=="xfs" and data_label=="DATA12","hint":"lvdata deve ter >=1,4 GiB, XFS e DATA12."},
 {"label":"lvdata está montado e persistente por UUID","pass":fm_rc==0 and "xfs" in fm and "/srv/data12" in fm and data_fstab,"hint":"Monte /srv/data12 e use UUID no fstab."},
 {"label":"lvswap está configurado e ativo","pass":sizes.get("lvswap",0)>=500 and swap_type=="swap" and swap_label=="SWAP12" and swap_active,"hint":"Crie, formate e ative lvswap."},
 {"label":"swap está persistente por UUID e fstab é válido","pass":swap_fstab and verify_rc==0,"hint":"Use UUID para swap e valide o fstab."},
 {"label":"evidências foram salvas","pass":"vdb" in read("lsblk.txt") and "vg12" in read("lvm.txt") and "/srv/data12" in read("findmnt.txt") and ("Filename" in read("swap.txt") or "NAME" in read("swap.txt")) and (root/"verify.txt").is_file(),"hint":"Salve todas as evidências pedidas."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj12-03","checks":checks,"score":score},ensure_ascii=False))
"""

def main():
    p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
    r=json_from_remote_python("servera",REMOTE_CHECKER)
    print(json.dumps(r,ensure_ascii=False))
    return 0 if r["score"]==100 else 1
if __name__=="__main__":
    raise SystemExit(main())
