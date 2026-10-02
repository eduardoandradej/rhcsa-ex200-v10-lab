#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json, subprocess

root=Path("/home/student/rhcsa-lab/obj05-01/output")

def pidfile(name):
    try:
        return int(Path(name).read_text().strip())
    except Exception:
        return None

def psline(pid):
    if not pid:
        return None
    p=subprocess.run(
        ["ps","-o","pid=,ppid=,stat=,ni=,args=","-p",str(pid)],
        text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE
    )
    return p.stdout if p.returncode==0 else None

spid=pidfile("/run/rhcsa-proc-sleeper.pid")
tpid=pidfile("/run/rhcsa-proc-stopped.pid")
sexp=psline(spid)
texp=psline(tpid)

def exact(path, expected):
    p=root/path
    return expected is not None and p.is_file() and p.read_text()==expected

checks=[
 {"label":"relatório do processo sleeper está correto","pass":exact("sleeper.txt",sexp),"hint":"Use ps com as colunas pid,ppid,stat,ni,args e o PID do sleeper."},
 {"label":"relatório do processo stopped está correto","pass":exact("stopped.txt",texp),"hint":"Use ps com as mesmas colunas e o PID do processo stopped."},
 {"label":"processo sleeper permanece em estado não parado","pass":bool(sexp and "rhcsa-proc-sleeper" in sexp and "T" not in sexp.split()[2]),"hint":"Não suspenda o sleeper."},
 {"label":"processo stopped permanece parado","pass":bool(texp and "T" in texp.split()[2]),"hint":"O processo preparado deve continuar em estado T."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj05-01","checks":checks,"score":score},ensure_ascii=False))
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
