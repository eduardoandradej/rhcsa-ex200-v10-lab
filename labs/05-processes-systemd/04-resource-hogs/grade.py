#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json

root=Path("/home/student/rhcsa-lab/obj05-04/output")

def pid(path):
    try:
        return int(Path(path).read_text().strip())
    except Exception:
        return None

cpid=pid("/run/rhcsa-cpu-hog.pid")
mpid=pid("/run/rhcsa-mem-hog.pid")
cpu=(root/"cpu-before.txt").read_text(errors="replace") if (root/"cpu-before.txt").is_file() else ""
mem=(root/"memory-before.txt").read_text(errors="replace") if (root/"memory-before.txt").is_file() else ""

checks=[
 {"label":"snapshot do processo CPU foi salvo","pass":bool(cpid and str(cpid) in cpu and "rhcsa-cpu-hog" in cpu),"hint":"Capture a linha do PID do CPU hog antes de terminá-lo."},
 {"label":"snapshot do processo de memória foi salvo","pass":bool(mpid and str(mpid) in mem and "rhcsa-mem-hog" in mem),"hint":"Capture a linha do PID do memory hog antes de terminá-lo."},
 {"label":"CPU hog foi encerrado","pass":bool(cpid and not Path(f"/proc/{cpid}").exists()),"hint":"Envie SIGTERM para o CPU hog."},
 {"label":"memory hog foi encerrado","pass":bool(mpid and not Path(f"/proc/{mpid}").exists()),"hint":"Envie SIGTERM para o memory hog."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj05-04","checks":checks,"score":score},ensure_ascii=False))
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
