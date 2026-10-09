#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json,subprocess,re
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

_,pt=run(["sudo","-n","parted","-sm","/dev/vdb","unit","B","print"])
_,u1=run(["sudo","-n","blkid","-s","UUID","-o","value","/dev/vdb1"])
_,u2=run(["sudo","-n","blkid","-s","UUID","-o","value","/dev/vdb2"])
_,t1=run(["sudo","-n","blkid","-s","TYPE","-o","value","/dev/vdb1"])
_,t2=run(["sudo","-n","blkid","-s","TYPE","-o","value","/dev/vdb2"])
_,l1=run(["sudo","-n","blkid","-s","LABEL","-o","value","/dev/vdb1"])
_,l2=run(["sudo","-n","blkid","-s","LABEL","-o","value","/dev/vdb2"])
_,mnt=run(["findmnt","-n","-o","SOURCE,FSTYPE","/basicdata"])
active=active_swap_uuids()
baseline=baseline_swap_uuids("obj08-06")
_,fstab=run(["sudo","-n","cat","/etc/fstab"])
rc,_=run(["findmnt","--verify","--tab-file","/etc/fstab"])
marker=Path("/basicdata/marker.txt")
lines=[l for l in fstab.splitlines() if l.strip() and not l.lstrip().startswith("#")]
data=any(re.search(rf"^UUID={re.escape(u1)}\s+/basicdata\s+xfs\s+defaults\s+0\s+0$",l) for l in lines)
swap=any(re.search(rf"^UUID={re.escape(u2)}\s+none\s+swap\s+defaults\s+0\s+0$",l) for l in lines)
checks=[
 {"label":"GPT contém data e swap","pass":":gpt:" in pt and "basicdata" in pt and "basicswap" in pt,"hint":"Crie duas partições GPT."},
 {"label":"XFS e swap têm labels corretos","pass":t1=="xfs" and l1=="BASIC08" and t2=="swap" and l2=="BASWAP08","hint":"Formate os dois objetos."},
 {"label":"data está montado e persistente por UUID","pass":"xfs" in mnt and data,"hint":"Monte /basicdata usando UUID no fstab."},
 {"label":"swap está ativo e persistente por UUID","pass":bool(u2) and u2 in active and swap,"hint":"Ative e persista o swap por UUID."},
 {"label":"swap original foi preservado","pass":bool(baseline) and baseline.issubset(active),"hint":"Preserve o swap original."},
 {"label":"marker está no filesystem e fstab é válido","pass":marker.is_file() and "OBJ08-BASIC" in marker.read_text(errors="replace") and rc==0,"hint":"Crie marker.txt e valide fstab."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj08-06","checks":checks,"score":score},ensure_ascii=False))
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
