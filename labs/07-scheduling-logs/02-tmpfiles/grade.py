#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json
import subprocess

def run(args):
    p = subprocess.run(
        args,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return p.returncode, p.stdout.strip()

def sudo_cat(path):
    rc, out = run(["sudo", "-n", "cat", path])
    return out if rc == 0 else ""

def privileged_absent(path):
    # The parent directory is root:root 0700. A student process cannot even
    # stat children below it, so existence must be checked with privilege.
    rc, _ = run(["sudo", "-n", "test", "!", "-e", path])
    return rc == 0

cfg = sudo_cat("/etc/tmpfiles.d/rhcsa-momentary.conf")
_, st = run(["stat", "-c", "%a %U %G", "/run/rhcsa-momentary"])

out = Path("/home/student/rhcsa-lab/obj07-02/output/stat.txt")

checks = [
    {
        "label": "regra tmpfiles correta",
        "pass": "d /run/rhcsa-momentary 0700 root root 30s" in cfg,
        "hint": "Crie a regra d.",
    },
    {
        "label": "diretório correto",
        "pass": st == "700 root root",
        "hint": "Aplique --create.",
    },
    {
        "label": "stale.txt removido",
        "pass": privileged_absent("/run/rhcsa-momentary/stale.txt"),
        "hint": "Use --clean.",
    },
    {
        "label": "stat salvo",
        "pass": (
            out.is_file()
            and "700 root root" in out.read_text(errors="replace")
        ),
        "hint": "Salve stat.txt.",
    },
]

score = round(sum(c["pass"] for c in checks) / len(checks) * 100)
print(json.dumps(
    {"lab_id": "obj07-02", "checks": checks, "score": score},
    ensure_ascii=False,
))
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.parse_args()

    result = json_from_remote_python("servera", REMOTE_CHECKER)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["score"] == 100 else 1

if __name__ == "__main__":
    raise SystemExit(main())
