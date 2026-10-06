#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj06-05
sudo python3 - <<'PY2'
from pathlib import Path
p=Path('/etc/NetworkManager/system-connections/ex200-keyfile.nmconnection')
s=p.read_text()
if '10.66.5.110/24' not in s:
    s=s.replace('address1=10.66.5.10/24','address1=10.66.5.10/24\naddress2=10.66.5.110/24')
p.write_text(s)
PY2
sudo nmcli con reload
sudo nmcli con up ex200-keyfile
ip -4 -br addr show ex200a > output/runtime.txt
EOS
