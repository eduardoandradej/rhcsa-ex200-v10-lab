#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj06-04
sudo nmcli con add con-name ex200-dual type ethernet ifname ex200a ipv4.method manual ipv4.addresses 10.66.4.10/24 ipv6.method manual ipv6.addresses fd00:66:4::10/64 connection.autoconnect yes
sudo nmcli con up ex200-dual
ping -c 2 10.66.4.254 > output/ping4.txt
ping -6 -c 2 fd00:66:4::fe > output/ping6.txt
EOS
