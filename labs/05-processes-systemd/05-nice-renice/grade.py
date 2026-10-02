#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json, subprocess

root=Path("/home/student/rhcsa-lab/obj05-05")

def pid(name):
    try:
        return int((root/"output"/name).read_text().strip())
    except Exception:
        return None

def info(p):
    if not p:
        return None
    x=subprocess.run(
        ["ps","-o","pid=,ni=,stat=,args=","-p",str(p)],
        text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE
    )
    if x.returncode != 0 or not x.stdout.strip():
        return None
    parts=x.stdout.split(None,3)
    return {
        "pid": int(parts[0]),
        "nice": int(parts[1]),
        "stat": parts[2],
        "args": parts[3] if len(parts)>3 else ""
    }

p1=pid("nice-start.pid")
p2=pid("nice-change.pid")
i1=info(p1); i2=info(p2)
report=(root/"output/priorities.txt").read_text(errors="replace") if (root/"output/priorities.txt").is_file() else ""

checks=[
 {"label":"nice-start foi iniciado com nice 12","pass":bool(i1 and i1["nice"]==12 and "rhcsa-nice-start" in i1["args"]),"hint":"Use nice -n 12 ao iniciar o primeiro processo."},
 {"label":"nice-change foi ajustado para nice 7","pass":bool(i2 and i2["nice"]==7 and "rhcsa-nice-change" in i2["args"]),"hint":"Inicie normalmente e depois use renice -n 7 -p PID."},
 {"label":"relatório de prioridades contém os dois processos","pass":bool(p1 and p2 and str(p1) in report and str(p2) in report and "rhcsa-nice-start" in report and "rhcsa-nice-change" in report),"hint":"Salve ps com pid,ni,stat,args dos dois PIDs."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj05-05","checks":checks,"score":score},ensure_ascii=False))
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
