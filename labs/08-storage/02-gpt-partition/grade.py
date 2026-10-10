#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
import json
import subprocess
from pathlib import Path

def run(args):
    p = subprocess.run(
        args,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return p.returncode, p.stdout.strip()

def bytes_value(value):
    value = (value or "").strip()
    if value.endswith("B"):
        value = value[:-1]
    try:
        return int(value)
    except ValueError:
        return 0

# `parted -m` is authoritative for the GPT partition name.  Do not depend on
# unprivileged lsblk PARTLABEL visibility: device-node/udev permissions can
# make that column transiently unavailable even while the GPT metadata is
# correct.
pt_rc, pt = run([
    "sudo", "-n", "parted", "-sm",
    "/dev/vdb", "unit", "B", "print",
])

partition = None
for line in pt.splitlines():
    line = line.strip()
    if not line or not line[0].isdigit():
        continue
    fields = line.rstrip(";").split(":")
    if fields and fields[0] == "1" and len(fields) >= 6:
        partition = fields
        break

size_b = bytes_value(partition[3]) if partition else 0
part_name = partition[5] if partition else ""

# Keep lsblk for topology and filesystem-state inspection, but run it with
# sudo and do not use PARTLABEL as the source of truth for the GPT name.
ls_rc, ls = run([
    "sudo", "-n", "lsblk", "-J", "-b",
    "-o", "NAME,SIZE,TYPE,FSTYPE",
    "/dev/vdb",
])

try:
    tree = json.loads(ls).get("blockdevices", [])
except json.JSONDecodeError:
    tree = []

parts = []
for disk in tree:
    parts.extend(disk.get("children") or [])

vdb1 = next((x for x in parts if x.get("name") == "vdb1"), None)

okpart = (
    pt_rc == 0
    and partition is not None
    and 950 * 1024**2 <= size_b <= 1100 * 1024**2
    and part_name == "data08"
    and vdb1 is not None
    and vdb1.get("type") == "part"
)

checks = [
    {
        "label": "tabela GPT criada",
        "pass": pt_rc == 0 and ":gpt:" in pt,
        "hint": "Use parted mklabel gpt.",
    },
    {
        "label": "vdb1 tem tamanho e nome corretos",
        "pass": okpart,
        "hint": "Crie data08 entre 1MiB e 1025MiB.",
    },
    {
        "label": "nenhum filesystem foi criado",
        "pass": (
            ls_rc == 0
            and bool(parts)
            and all(not (x.get("fstype") or "") for x in parts)
        ),
        "hint": "Não execute mkfs neste lab.",
    },
    {
        "label": "evidências foram salvas",
        "pass": all(
            Path(
                "/home/student/rhcsa-lab/obj08-02/output/" + name
            ).is_file()
            for name in ["parted.txt", "lsblk.txt"]
        ),
        "hint": "Salve parted.txt e lsblk.txt.",
    },
]

score = round(sum(c["pass"] for c in checks) / len(checks) * 100)
print(json.dumps(
    {"lab_id": "obj08-02", "checks": checks, "score": score},
    ensure_ascii=False,
))
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
