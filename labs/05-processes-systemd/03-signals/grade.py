#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json, os

def pid(name):
    try:
        return int(Path(f"/run/rhcsa-signal-{name}.pid").read_text().strip())
    except Exception:
        return None

def state(p):
    if not p or not Path(f"/proc/{p}/stat").exists():
        return None
    try:
        return Path(f"/proc/{p}/stat").read_text().split()[2]
    except Exception:
        return None

a=pid("alpha"); b=pid("beta"); g=pid("gamma")
sa=state(a); sb=state(b); sg=state(g)

checks=[
 {"label":"alpha recebeu stop e está parado","pass":sa in {"T","t"},"hint":"Envie SIGSTOP para o PID de alpha."},
 {"label":"beta foi terminado","pass":sb is None,"hint":"Envie SIGTERM para beta e aguarde o encerramento."},
 {"label":"gamma foi retomado","pass":sg is not None and sg not in {"T","t"},"hint":"Envie SIGCONT para gamma."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj05-03","checks":checks,"score":score},ensure_ascii=False))
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
