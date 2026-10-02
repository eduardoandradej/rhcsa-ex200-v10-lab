#!/usr/bin/env bash
set -Eeuo pipefail

ssh serverb 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj03-08

sudo tee /etc/yum.repos.d/rhcsa-system.repo >/dev/null <<'EOF'
[rhcsa-system-base]
name=RHCSA System Base
baseurl=file:///var/lib/rhcsa-lab/obj03/repos/base
enabled=1
gpgcheck=0

[rhcsa-system-errata]
name=RHCSA System Errata
baseurl=file:///var/lib/rhcsa-lab/obj03/repos/errata
enabled=0
gpgcheck=0
EOF

sudo dnf -y --disablerepo='*' \
  --enablerepo=rhcsa-system-base \
  install rhcsa-system-1.0-1

rpm -qpi assets/rhcsa-local-1.0-1.noarch.rpm \
  > output/local-rpm-info.txt

sudo dnf -y install ./assets/rhcsa-local-1.0-1.noarch.rpm

sudo python3 - <<'PY'
from pathlib import Path
p=Path("/etc/yum.repos.d/rhcsa-system.repo")
lines=p.read_text().splitlines()
out=[]
section=None
for line in lines:
    if line.startswith("[") and line.endswith("]"):
        section=line[1:-1]
    if section=="rhcsa-system-errata" and line.startswith("enabled="):
        line="enabled=1"
    out.append(line)
p.write_text("\n".join(out)+"\n")
PY

sudo dnf -y --disablerepo='*' \
  --enablerepo=rhcsa-system-base \
  --enablerepo=rhcsa-system-errata \
  upgrade rhcsa-system

sudo python3 - <<'PY'
from pathlib import Path
p=Path("/etc/yum.repos.d/rhcsa-system.repo")
lines=p.read_text().splitlines()
p.write_text(
    "\n".join(
        "enabled=0" if x.startswith("enabled=") else x
        for x in lines
    ) + "\n"
)
PY

id="$(
  dnf history list rhcsa-system \
    | awk '$1 ~ /^[0-9]+$/ {print $1; exit}'
)"

test -n "$id"
dnf history info "$id" > output/history.txt
EOS
