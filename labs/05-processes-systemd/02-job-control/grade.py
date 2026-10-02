#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json, os, subprocess

root=Path("/home/student/rhcsa-lab/obj05-02")

def readpid(name):
    try:
        return int((root/"output"/name).read_text().strip())
    except Exception:
        return None

def proc(pid):
    if not pid:
        return None
    p=subprocess.run(
        ["ps","-o","pid=,stat=,args=","-p",str(pid)],
        text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE
    )
    return p.stdout if p.returncode==0 else None

ap=readpid("alpha.pid")
bp=readpid("beta.pid")
a=proc(ap)
b=proc(bp)
jobs=(root/"output/jobs.txt").read_text(errors="replace") if (root/"output/jobs.txt").is_file() else ""
procs=(root/"output/processes.txt").read_text(errors="replace") if (root/"output/processes.txt").is_file() else ""

astate=a.split()[1] if a else ""
bstate=b.split()[1] if b else ""

checks=[
 {"label":"PIDs dos dois jobs foram registrados","pass":bool(ap and bp and ap!=bp),"hint":"Grave $! após iniciar cada job."},
 {"label":"job-alpha está parado","pass":bool(a and "rhcsa-job-alpha" in a and "T" in astate),"hint":"Suspenda alpha usando controle de jobs."},
 {"label":"job-beta permanece executando em background","pass":bool(b and "rhcsa-job-beta" in b and "T" not in bstate),"hint":"Deixe beta em background sem suspendê-lo."},
 {"label":"jobs -l registrou os dois jobs e seus estados","pass":str(ap) in jobs and str(bp) in jobs and "Stopped" in jobs and "Running" in jobs,"hint":"Salve jobs -l enquanto ambos ainda pertencem à mesma sessão shell."},
 {"label":"relatório ps contém os dois PIDs","pass":str(ap) in procs and str(bp) in procs and "rhcsa-job-alpha" in procs and "rhcsa-job-beta" in procs,"hint":"Use ps sobre os dois PIDs."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj05-02","checks":checks,"score":score},ensure_ascii=False))
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.parse_args()

    payload = json_from_remote_python("servera", REMOTE_CHECKER)
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload["score"] == 100 else 1

if __name__ == "__main__":
    raise SystemExit(main())
