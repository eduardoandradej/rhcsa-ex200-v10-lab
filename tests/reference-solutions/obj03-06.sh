#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'sudo bash -Eeuo pipefail -s' <<'EOS'
python3 - <<'PY'
from pathlib import Path
p=Path("/etc/yum.repos.d/rhcsa-update.repo")
lines=p.read_text().splitlines()
out=[]
section=None
for line in lines:
    if line.startswith("[") and line.endswith("]"):
        section=line[1:-1]
    if section=="rhcsa-errata" and line.startswith("enabled="):
        line="enabled=1"
    out.append(line)
p.write_text("\n".join(out)+"\n")
PY

dnf -y --disablerepo='*' \
  --enablerepo=rhcsa-base \
  --enablerepo=rhcsa-errata \
  upgrade rhcsa-update-demo

python3 - <<'PY'
from pathlib import Path
p=Path("/etc/yum.repos.d/rhcsa-update.repo")
lines=p.read_text().splitlines()
p.write_text("\n".join("enabled=0" if x.startswith("enabled=") else x for x in lines)+"\n")
PY
EOS
