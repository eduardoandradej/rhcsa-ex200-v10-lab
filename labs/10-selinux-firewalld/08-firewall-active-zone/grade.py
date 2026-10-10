#!/usr/bin/env python3
import argparse,json
from labctl.remote import json_from_remote_python
REMOTE_CHECKER=r"""
from pathlib import Path
import subprocess,json
root=Path("/home/student/rhcsa-lab/obj10-08/output")
def run(args):
 p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE); return p.returncode,p.stdout.strip()
_,iface=run(["bash","-lc","ip -o route show default | awk '{print $5; exit}'"])
_,zone=run(["sudo","-n","firewall-cmd",f"--get-zone-of-interface={iface}"])
if not zone or zone=="no zone":
 _,zone=run(["sudo","-n","firewall-cmd","--get-default-zone"])
r_rc,r=run(["sudo","-n","firewall-cmd",f"--zone={zone}","--query-port=45102/tcp"])
p_rc,p=run(["sudo","-n","firewall-cmd","--permanent",f"--zone={zone}","--query-port=45102/tcp"])
def read(n):
 q=root/n; return q.read_text(errors="replace").strip() if q.is_file() else ""
checks=[
 {"label":"zona ativa foi identificada corretamente","pass":read("zone.txt")==zone and bool(zone),"hint":"Use a interface da rota padrão."},
 {"label":"porta existe em runtime","pass":r_rc==0 and r=="yes","hint":"Recarregue após configurar permanentemente."},
 {"label":"porta existe no permanente","pass":p_rc==0 and p=="yes","hint":"Use --permanent."},
 {"label":"evidências foram salvas","pass":read("runtime.txt")=="yes" and read("permanent.txt")=="yes","hint":"Salve as consultas."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj10-08","checks":checks,"score":score},ensure_ascii=False))
"""
def main():
 p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
 r=json_from_remote_python("servera",REMOTE_CHECKER); print(json.dumps(r,ensure_ascii=False)); return 0 if r["score"]==100 else 1
if __name__=="__main__": raise SystemExit(main())
