#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json, subprocess, re

root = Path("/home/student/rhcsa-lab/obj09-05/output")

def run(args):
    p = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.returncode, p.stdout.strip()

_, uuid = run(["sudo", "-n", "blkid", "-s", "UUID", "-o", "value", "/dev/vdb1"])
_, fstab = run(["sudo", "-n", "cat", "/etc/fstab"])
_, mounted = run(["findmnt", "-n", "-o", "SOURCE,FSTYPE,TARGET", "/srv/recovery09"])
verify_rc, _ = run(["findmnt", "--verify", "--tab-file", "/etc/fstab"])

lines = [l for l in fstab.splitlines() if l.strip() and not l.lstrip().startswith("#")]
target_lines = [l for l in lines if re.search(r"\s/srv/recovery09\s", l)]
correct = any(
    re.search(
        rf"^UUID={re.escape(uuid)}\s+/srv/recovery09\s+xfs\s+defaults\s+0\s+0\s*$",
        l
    )
    for l in target_lines
)

findmnt_file = root / "findmnt.txt"
verify_file = root / "verify.txt"
saved_findmnt = findmnt_file.read_text(errors="replace") if findmnt_file.is_file() else ""

checks = [
    {"label":"fstab usa UUID correto e estado final defaults",
     "pass":bool(uuid) and correct,
     "hint":"Use UUID=<uuid> /srv/recovery09 xfs defaults 0 0."},
    {"label":"nofail foi removido do estado final",
     "pass":bool(target_lines) and all("nofail" not in l for l in target_lines),
     "hint":"nofail é apenas a proteção inicial deste lab."},
    {"label":"filesystem XFS está montado no destino correto",
     "pass":"xfs" in mounted and "/srv/recovery09" in mounted,
     "hint":"Crie o mount point e use mount -a."},
    {"label":"fstab passa em findmnt --verify",
     "pass":verify_rc == 0,
     "hint":"Corrija todos os erros de /etc/fstab."},
    {"label":"evidências foram salvas",
     "pass":"/srv/recovery09" in saved_findmnt and verify_file.is_file(),
     "hint":"Salve findmnt e a validação em output/."},
]
score = round(sum(c["pass"] for c in checks) / len(checks) * 100)
print(json.dumps({"lab_id":"obj09-05","checks":checks,"score":score}, ensure_ascii=False))
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
