#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
import json,subprocess,re
dev="/dev/rhcsa_vgswap/rhcsa_lvswap"
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

_,typ=run(["sudo","-n","blkid","-s","TYPE","-o","value",dev])
_,label=run(["sudo","-n","blkid","-s","LABEL","-o","value",dev])
_,uuid=run(["sudo","-n","blkid","-s","UUID","-o","value",dev])
active=active_swap_uuids()
baseline=baseline_swap_uuids("obj08-11")
_,fstab=run(["sudo","-n","cat","/etc/fstab"])
_,lv=run(["sudo","-n","lvs","rhcsa_vgswap/rhcsa_lvswap","--noheadings","--units","b","-o","lv_size"])
try: size=int(float(lv.strip().rstrip("B")))
except: size=0
lines=[l for l in fstab.splitlines() if l.strip() and not l.lstrip().startswith("#")]
match=any(re.search(rf"^UUID={re.escape(uuid)}\s+none\s+swap\s+defaults\s+0\s+0$",l) for l in lines)
checks=[
 {"label":"LV swap tem tamanho correto","pass":700*1024**2 <= size <= 820*1024**2,"hint":"Crie LV de 768M."},
 {"label":"LV foi inicializado como swap","pass":typ=="swap" and label=="LVSWAP08","hint":"Use mkswap -L LVSWAP08."},
 {"label":"novo swap LVM está ativo por UUID","pass":bool(uuid) and uuid in active,"hint":"Ative o LV swap."},
 {"label":"swap original foi preservado","pass":bool(baseline) and baseline.issubset(active),"hint":"Não desative o swap original."},
 {"label":"persistência usa UUID","pass":match,"hint":"Adicione UUID no fstab."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj08-11","checks":checks,"score":score},ensure_ascii=False))
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
