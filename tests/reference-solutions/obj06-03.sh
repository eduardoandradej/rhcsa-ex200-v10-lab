#!/usr/bin/env bash
set -Eeuo pipefail

ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj06-03

sudo nmcli con mod ex200-mod \
  ipv4.addresses 10.66.3.20/24 \
  +ipv4.addresses 10.66.3.120/24 \
  ipv4.never-default yes \
  connection.autoconnect yes

# never-default and gateway are mutually exclusive in NetworkManager.
sudo nmcli con mod ex200-mod ipv4.gateway ""

sudo nmcli con up ex200-mod

nmcli -f connection.id,connection.autoconnect,ipv4.method,ipv4.addresses,ipv4.gateway,ipv4.never-default \
  con show ex200-mod > output/profile.txt

ip -4 -br addr show ex200a > output/runtime.txt
ping -c 2 10.66.3.254 > output/ping.txt
EOS
