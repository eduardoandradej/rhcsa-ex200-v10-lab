#!/usr/bin/env python3
import argparse,json
from labctl.remote import json_from_remote_python
REMOTE_CHECKER=r"""
from pathlib import Path
import subprocess,json
root=Path("/home/student/rhcsa-lab/obj11-05/output")
def read(n):
 p=root/n; return p.read_text(errors="replace").strip() if p.is_file() else ""
def run(args):
 p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE); return p.returncode,p.stdout.strip()
fstab=Path("/etc/fstab").read_text(errors="replace").splitlines()
entry=[]
for line in fstab:
 fields=line.split()
 if len(fields)>=4 and fields[0]=="serverb:/srv/rhcsa11/systemd" and fields[1]=="/mnt/rhcsa11-auto" and fields[2]=="nfs":
  entry=fields; break
opts=set(entry[3].split(",")) if entry else set()
_,unit=run(["systemd-escape","--path","--suffix=automount","/mnt/rhcsa11-auto"])
svc_rc,_=run(["systemctl","is-active","--quiet",unit])
fm=read("findmnt.txt")
checks=[
 {"label":"fstab contém x-systemd.automount","pass":bool(entry) and {"rw","sync","x-systemd.automount"}.issubset(opts),"hint":"Adicione a entrada com x-systemd.automount."},
 {"label":"unidade automount está ativa","pass":svc_rc==0 and read("unit.txt")=="active","hint":"Inicie a unidade gerada pelo systemd."},
 {"label":"acesso disparou a montagem NFS","pass":"serverb:/srv/rhcsa11/systemd" in fm and "nfs" in fm,"hint":"Acesse hello.txt depois de iniciar a automount."},
 {"label":"conteúdo remoto foi validado","pass":read("content.txt")=="OBJ11 systemd automount","hint":"Leia hello.txt."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj11-05","checks":checks,"score":score},ensure_ascii=False))
"""
def main():
 p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
 r=json_from_remote_python("servera",REMOTE_CHECKER); print(json.dumps(r,ensure_ascii=False)); return 0 if r["score"]==100 else 1
if __name__=="__main__": raise SystemExit(main())
