#!/usr/bin/env python3
import argparse,json
from labctl.remote import json_from_remote_python
REMOTE_CHECKER=r"""
from pathlib import Path
import subprocess,json
root=Path("/home/student/rhcsa-lab/obj11-02/output")
def read(n):
 p=root/n; return p.read_text(errors="replace").strip() if p.is_file() else ""
def run(args):
 p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE); return p.returncode,p.stdout.strip()
fstab=Path("/etc/fstab").read_text(errors="replace").splitlines()
entry=[]
for line in fstab:
 fields=line.split()
 if len(fields)>=4 and fields[0]=="serverb:/srv/rhcsa11/persist" and fields[1]=="/mnt/rhcsa11-persist" and fields[2]=="nfs":
  entry=fields; break
opts=set(entry[3].split(",")) if entry else set()
rc,source=run(["findmnt","-n","-o","SOURCE,FSTYPE","/mnt/rhcsa11-persist"])
verify_rc,_=run(["sudo","-n","findmnt","--verify"])
checks=[
 {"label":"fstab contém a montagem NFS correta","pass":bool(entry) and {"rw","sync"}.issubset(opts),"hint":"Use serverb:/srv/rhcsa11/persist ... nfs rw,sync 0 0."},
 {"label":"NFS está montado no destino correto","pass":rc==0 and "serverb:/srv/rhcsa11/persist" in source and "nfs" in source,"hint":"Monte pelo ponto definido no fstab."},
 {"label":"fstab passa em findmnt --verify","pass":verify_rc==0,"hint":"Corrija o fstab antes de concluir."},
 {"label":"conteúdo remoto foi validado","pass":read("content.txt")=="OBJ11 persistent NFS","hint":"Leia hello.txt."},
 {"label":"evidências foram salvas","pass":"serverb:/srv/rhcsa11/persist" in read("findmnt.txt") and (root/"verify.txt").is_file(),"hint":"Salve findmnt.txt e verify.txt."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj11-02","checks":checks,"score":score},ensure_ascii=False))
"""
def main():
 p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
 r=json_from_remote_python("servera",REMOTE_CHECKER); print(json.dumps(r,ensure_ascii=False)); return 0 if r["score"]==100 else 1
if __name__=="__main__": raise SystemExit(main())
