#!/usr/bin/env python3
import argparse,json,re,subprocess
from pathlib import Path
from labctl.remote import json_from_remote_python

REMOTE_CHECKER=r"""
from pathlib import Path
import subprocess,json,re
root=Path("/home/student/rhcsa-lab/obj12-04/output")
def run(args):
    p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return p.returncode,p.stdout.strip()
def read(n):
    p=root/n
    return p.read_text(errors="replace").strip() if p.is_file() else ""

_,target=run(["systemctl","get-default"])
gr_rc,grubby=run(["sudo","-n","grubby","--info=ALL"])
blocks=[b for b in re.split(r"(?=^index=)",grubby,flags=re.M) if b.strip()]
kblocks=[b for b in blocks if re.search(r"^kernel=",b,re.M)]
all_have=bool(kblocks) and all(
    any("systemd.show_status=1" in ln for ln in b.splitlines() if ln.startswith("args="))
    for b in kblocks
)

fstab=Path("/etc/fstab").read_text(errors="replace").splitlines()
entry=[]
for line in fstab:
    fields=line.split()
    if len(fields)>=4 and fields[0]=="tmpfs" and fields[1]=="/srv/boot12" and fields[2]=="tmpfs":
        entry=fields; break
opts=set(entry[3].split(",")) if entry else set()
fm_rc,fm=run(["findmnt","-n","-o","SOURCE,FSTYPE,TARGET,OPTIONS","/srv/boot12"])
verify_rc,_=run(["sudo","-n","findmnt","--verify"])

checks=[
 {"label":"target padrão é multi-user.target","pass":target=="multi-user.target","hint":"Use systemctl set-default multi-user.target."},
 {"label":"argumento persistente está em todas as entradas","pass":gr_rc==0 and all_have,"hint":"Use grubby --update-kernel=ALL."},
 {"label":"fstab contém tmpfs com opções exigidas","pass":bool(entry) and {"rw","nosuid","nodev"}.issubset(opts),"hint":"Configure tmpfs /srv/boot12 no fstab."},
 {"label":"tmpfs está montado em /srv/boot12","pass":fm_rc==0 and "tmpfs" in fm and "/srv/boot12" in fm,"hint":"Monte o ponto após daemon-reload."},
 {"label":"fstab é válido","pass":verify_rc==0,"hint":"Use findmnt --verify."},
 {"label":"evidências foram salvas","pass":read("target.txt")=="multi-user.target" and "systemd.show_status=1" in read("grubby.txt") and "/srv/boot12" in read("findmnt.txt") and (root/"verify.txt").is_file(),"hint":"Salve target, grubby, findmnt e verify."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj12-04","checks":checks,"score":score},ensure_ascii=False))
"""

def main():
    p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
    r=json_from_remote_python("servera",REMOTE_CHECKER)
    print(json.dumps(r,ensure_ascii=False))
    return 0 if r["score"]==100 else 1
if __name__=="__main__":
    raise SystemExit(main())
