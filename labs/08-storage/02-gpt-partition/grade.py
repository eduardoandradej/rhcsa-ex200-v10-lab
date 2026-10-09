#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
import json,subprocess
def run(a):
 p=subprocess.run(a,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 return p.returncode,p.stdout.strip()
_,pt=run(["sudo","-n","parted","-sm","/dev/vdb","unit","B","print"])
_,ls=run(["lsblk","-J","-b","-o","NAME,SIZE,TYPE,FSTYPE,PARTLABEL","/dev/vdb"])
import json as _json
tree=_json.loads(ls).get("blockdevices",[])
parts=[]
for disk in tree:
 parts.extend(disk.get("children") or [])
okpart=False
for x in parts:
 if x.get("name")=="vdb1":
  size=int(x.get("size") or 0); label=x.get("partlabel") or ""
  okpart=(950*1024**2 <= size <= 1100*1024**2 and label=="data08")
checks=[
 {"label":"tabela GPT criada","pass":":gpt:" in pt,"hint":"Use parted mklabel gpt."},
 {"label":"vdb1 tem tamanho e nome corretos","pass":okpart,"hint":"Crie data08 entre 1MiB e 1025MiB."},
 {"label":"nenhum filesystem foi criado","pass":all(not (x.get("fstype") or "") for x in parts),"hint":"Não execute mkfs neste lab."},
 {"label":"evidências foram salvas","pass":all(__import__("pathlib").Path("/home/student/rhcsa-lab/obj08-02/output/"+n).is_file() for n in ["parted.txt","lsblk.txt"]),"hint":"Salve parted.txt e lsblk.txt."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj08-02","checks":checks,"score":score},ensure_ascii=False))
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
