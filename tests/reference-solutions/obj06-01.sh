#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj06-01
nmcli device status > output/devices.txt
nmcli connection show > output/connections.txt
nmcli connection show --active > output/active.txt
ip -br link show ex200a > output/ex200a-link.txt
EOS
