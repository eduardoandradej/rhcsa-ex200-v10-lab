#!/usr/bin/env python3
import argparse,json
from labctl.remote import json_from_remote_python
REMOTE_CHECKER=r"""
from pathlib import Path
import subprocess,json
root=Path("/home/student/rhcsa-lab/obj11-01/output")
def read(n):
 p=root/n; return p.read_text(errors="replace").strip() if p.is_file() else ""
def run(args):
 p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE); return p.returncode,p.stdout.strip()
mount_rc,_=run(["findmnt","/mnt/rhcsa11-manual"])
checks=[
 {"label":"exportações do serverb foram consultadas","pass":"/srv/rhcsa11/manual" in read("exports.txt"),"hint":"Use showmount --exports serverb."},
 {"label":"evidência do mount NFS foi salva","pass":"serverb:/srv/rhcsa11/manual" in read("mount.txt") and ("nfs" in read("mount.txt")),"hint":"Salve findmnt enquanto estiver montado."},
 {"label":"conteúdo remoto foi lido","pass":read("content.txt")=="OBJ11 manual mount","hint":"Leia hello.txt no mount."},
 {"label":"estado final está desmontado","pass":mount_rc!=0 and read("unmounted.txt")=="unmounted","hint":"Finalize com umount."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj11-01","checks":checks,"score":score},ensure_ascii=False))
"""
def main():
 p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
 r=json_from_remote_python("servera",REMOTE_CHECKER); print(json.dumps(r,ensure_ascii=False)); return 0 if r["score"]==100 else 1
if __name__=="__main__": raise SystemExit(main())
