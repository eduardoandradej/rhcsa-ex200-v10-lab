#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json, subprocess

root=Path("/home/student/rhcsa-lab/obj05-10")

def run(args):
    p=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return p.returncode,p.stdout.strip()

try:
    rogue=int(Path("/run/rhcsa-rogue-cpu.pid").read_text().strip())
except Exception:
    rogue=None

try:
    batch=int((root/"output/batch.pid").read_text().strip())
except Exception:
    batch=None

rogue_report=(root/"output/rogue-before.txt").read_text(errors="replace") if (root/"output/rogue-before.txt").is_file() else ""
tuned_report=(root/"output/tuned-active.txt").read_text(errors="replace") if (root/"output/tuned-active.txt").is_file() else ""

batch_info=None
if batch:
    p=subprocess.run(
        ["ps","-o","ni=,args=","-p",str(batch)],
        text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE
    )
    if p.returncode==0 and p.stdout.strip():
        parts=p.stdout.strip().split(None,1)
        batch_info=(int(parts[0]), parts[1] if len(parts)>1 else "")

_,api_active=run(["systemctl","is-active","rhcsa-api.service"])
_,api_enabled=run(["systemctl","is-enabled","rhcsa-api.service"])
_,legacy_active=run(["systemctl","is-active","rhcsa-legacy.service"])
_,legacy_enabled=run(["systemctl","is-enabled","rhcsa-legacy.service"])
_,tuned_active=run(["tuned-adm","active"])

checks=[
 {"label":"rogue CPU foi identificado antes da finalização","pass":bool(rogue and str(rogue) in rogue_report and "rhcsa-rogue-cpu" in rogue_report),"hint":"Salve o ps do rogue antes de enviar o sinal."},
 {"label":"rogue CPU foi encerrado","pass":bool(rogue and not Path(f"/proc/{rogue}").exists()),"hint":"Envie SIGTERM ao rogue process."},
 {"label":"batch-worker executa com nice 10","pass":bool(batch_info and batch_info[0]==10 and "rhcsa-batch-worker" in batch_info[1]),"hint":"Inicie assets/batch-worker com nice -n 10 e grave $!."},
 {"label":"rhcsa-api está ativo e habilitado","pass":api_active=="active" and api_enabled=="enabled","hint":"Use systemctl enable --now rhcsa-api.service."},
 {"label":"rhcsa-legacy está inativo e mascarado","pass":legacy_active!="active" and legacy_enabled=="masked","hint":"Pare, desabilite e masque rhcsa-legacy.service."},
 {"label":"perfil TuneD balanced está ativo","pass":"balanced" in tuned_active and "balanced" in tuned_report,"hint":"Ative balanced e grave tuned-adm active."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj05-10","checks":checks,"score":score},ensure_ascii=False))
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.parse_args()

    payload = json_from_remote_python("serverb", REMOTE_CHECKER)
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload["score"] == 100 else 1

if __name__ == "__main__":
    raise SystemExit(main())
