#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json, subprocess, re

ARG = "systemd.show_status=1"
root = Path("/home/student/rhcsa-lab/obj09-07/output")

def run(args):
    p = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.returncode, p.stdout.strip()

def read(name):
    p = root / name
    return p.read_text(errors="replace").strip() if p.is_file() else ""

_, target = run(["systemctl", "get-default"])
_, grubby = run(["sudo", "-n", "grubby", "--info=ALL"])
verify_rc, _ = run(["findmnt", "--verify", "--tab-file", "/etc/fstab"])
cmdline = Path("/proc/cmdline").read_text().strip()

blocks = [b for b in re.split(r"(?=^index=)", grubby, flags=re.M) if b.strip()]
kernel_blocks = [b for b in blocks if re.search(r'^kernel=', b, re.M)]
all_have = bool(kernel_blocks) and all(
    any(ARG in line.split("=",1)[1] for line in b.splitlines() if line.startswith("args="))
    for b in kernel_blocks
)

checks = [
    {"label":"default target é multi-user.target",
     "pass":target == "multi-user.target",
     "hint":"Use systemctl set-default multi-user.target."},
    {"label":"argumento persistente existe em todas as entradas",
     "pass":all_have,
     "hint":"Atualize todas as entradas com grubby."},
    {"label":"fstab está consistente",
     "pass":verify_rc == 0,
     "hint":"Use findmnt --verify."},
    {"label":"evidência grubby salva",
     "pass":ARG in read("grubby.txt") and "index=" in read("grubby.txt"),
     "hint":"Salve grubby --info=ALL."},
    {"label":"evidência do target salva",
     "pass":read("default-target.txt") == "multi-user.target",
     "hint":"Salve systemctl get-default."},
    {"label":"cmdline do boot atual registrada sem falsificar estado futuro",
     "pass":read("current-cmdline.txt") == cmdline,
     "hint":"Grave exatamente /proc/cmdline; não invente o argumento persistente."},
    {"label":"evidência de verificação do fstab criada",
     "pass":(root / "fstab-verify.txt").is_file(),
     "hint":"Salve a saída de findmnt --verify."},
]
score = round(sum(c["pass"] for c in checks) / len(checks) * 100)
print(json.dumps({"lab_id":"obj09-07","checks":checks,"score":score}, ensure_ascii=False))
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
