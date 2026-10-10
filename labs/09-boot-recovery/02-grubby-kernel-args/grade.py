#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json, subprocess, re

ARG = "systemd.show_status=1"
out_file = Path("/home/student/rhcsa-lab/obj09-02/output/grubby.txt")

p = subprocess.run(
    ["sudo", "-n", "grubby", "--info=ALL"],
    text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
)
live = p.stdout.strip()
saved = out_file.read_text(errors="replace") if out_file.is_file() else ""

blocks = [b for b in re.split(r"(?=^index=)", live, flags=re.M) if b.strip()]
kernel_blocks = [b for b in blocks if re.search(r'^kernel=', b, re.M)]
all_have = bool(kernel_blocks) and all(
    any(ARG in line.split("=",1)[1] for line in b.splitlines() if line.startswith("args="))
    for b in kernel_blocks
)

checks = [
    {"label":"grubby consegue ler as entradas",
     "pass":p.returncode == 0 and bool(kernel_blocks),
     "hint":"Verifique grubby --info=ALL."},
    {"label":"argumento persistente presente em todas as entradas",
     "pass":all_have,
     "hint":"Use grubby --update-kernel=ALL --args=\"systemd.show_status=1\"."},
    {"label":"evidência final foi salva",
     "pass":ARG in saved and "index=" in saved,
     "hint":"Salve grubby --info=ALL em output/grubby.txt."},
]
score = round(sum(c["pass"] for c in checks) / len(checks) * 100)
print(json.dumps({"lab_id":"obj09-02","checks":checks,"score":score}, ensure_ascii=False))
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
