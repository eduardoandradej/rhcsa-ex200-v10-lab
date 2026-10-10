#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json, subprocess

def run(args):
    p = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.returncode, p.stdout.strip()

_, target = run(["systemctl", "get-default"])
_, link = run(["readlink", "-f", "/etc/systemd/system/default.target"])
p = Path("/home/student/rhcsa-lab/obj09-03/output/default-target.txt")
saved = p.read_text(errors="replace").strip() if p.is_file() else ""

checks = [
    {"label":"multi-user.target é o target padrão",
     "pass":target == "multi-user.target",
     "hint":"Use systemctl set-default multi-user.target."},
    {"label":"default.target aponta para multi-user.target",
     "pass":link.endswith("/multi-user.target"),
     "hint":"Verifique /etc/systemd/system/default.target."},
    {"label":"evidência do target foi salva",
     "pass":saved == "multi-user.target",
     "hint":"Grave systemctl get-default em output/default-target.txt."},
]
score = round(sum(c["pass"] for c in checks) / len(checks) * 100)
print(json.dumps({"lab_id":"obj09-03","checks":checks,"score":score}, ensure_ascii=False))
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
