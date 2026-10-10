#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json, subprocess

root = Path("/home/student/rhcsa-lab/obj09-01/output")

def run(args):
    p = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.returncode, p.stdout.strip()

def read(name):
    p = root / name
    return p.read_text(errors="replace").strip() if p.is_file() else ""

_, kernel = run(["uname", "-r"])
cmdline = Path("/proc/cmdline").read_text().strip()
_, default_kernel = run(["sudo", "-n", "grubby", "--default-kernel"])
_, grubby = run(["sudo", "-n", "grubby", "--info=ALL"])
_, target = run(["systemctl", "get-default"])

checks = [
    {"label":"kernel em execução registrado corretamente",
     "pass":read("kernel.txt") == kernel,
     "hint":"Grave uname -r em output/kernel.txt."},
    {"label":"linha de comando do boot atual registrada",
     "pass":read("cmdline.txt") == cmdline,
     "hint":"Grave /proc/cmdline em output/cmdline.txt."},
    {"label":"kernel padrão do boot loader registrado",
     "pass":read("default-kernel.txt") == default_kernel and bool(default_kernel),
     "hint":"Use grubby --default-kernel."},
    {"label":"inventário grubby contém o kernel padrão",
     "pass":default_kernel in read("grubby.txt") and "index=" in read("grubby.txt"),
     "hint":"Grave grubby --info=ALL em output/grubby.txt."},
    {"label":"target padrão do systemd registrado",
     "pass":read("default-target.txt") == target and target.endswith(".target"),
     "hint":"Use systemctl get-default."},
]
score = round(sum(c["pass"] for c in checks) / len(checks) * 100)
print(json.dumps({"lab_id":"obj09-01","checks":checks,"score":score}, ensure_ascii=False))
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
