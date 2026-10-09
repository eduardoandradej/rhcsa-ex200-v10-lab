#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
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

_,uuid=run(["sudo","-n","blkid","-s","UUID","-o","value","/dev/vde1"])
_,typ=run(["sudo","-n","blkid","-s","TYPE","-o","value","/dev/vde1"])
_,label=run(["sudo","-n","blkid","-s","LABEL","-o","value","/dev/vde1"])
active=active_swap_uuids()
baseline=baseline_swap_uuids("obj08-05")
_,fstab=run(["sudo","-n","cat","/etc/fstab"])
lines=[l for l in fstab.splitlines() if l.strip() and not l.lstrip().startswith("#")]
match=any(re.search(rf"^UUID={re.escape(uuid)}\s+none\s+swap\s+defaults\s+0\s+0\s*$",l) for l in lines)
checks=[
 {"label":"swap foi inicializado com label","pass":typ=="swap" and label=="RHCSA08SWAP","hint":"Use mkswap -L RHCSA08SWAP."},
 {"label":"novo swap está ativo por identidade UUID","pass":bool(uuid) and uuid in active,"hint":"Use swapon /dev/vde1."},
 {"label":"swap original foi preservado","pass":bool(baseline) and baseline.issubset(active),"hint":"Não desative o swap que já estava ativo antes do lab."},
 {"label":"swap persistente usa UUID","pass":bool(uuid) and match,"hint":"Adicione UUID no fstab."},
 {"label":"fstab não usa /dev/vde1 diretamente","pass":not any("/dev/vde1" in l and " swap " in (" "+l+" ") for l in lines),"hint":"Use UUID."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj08-05","checks":checks,"score":score},ensure_ascii=False))
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
