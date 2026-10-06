#!/usr/bin/env bash
set -Eeuo pipefail
ssh serverb 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj06-08
sudo nmcli con add con-name exam-net type ethernet ifname ex200a ipv4.method manual ipv4.addresses 10.66.8.20/24 ipv6.method manual ipv6.addresses fd00:66:8::20/64 connection.autoconnect yes
sudo nmcli con mod exam-net +ipv4.addresses 10.66.8.120/24
sudo nmcli con up exam-net
sudo hostnamectl set-hostname serverb-net.lab.test
echo '10.66.8.254 peer-net.lab.test peer-net' | sudo tee -a /etc/hosts >/dev/null
nmcli -f connection.id,connection.interface-name,connection.autoconnect,ipv4.method,ipv4.addresses,ipv6.method,ipv6.addresses con show exam-net > output/profile.txt
ip -br addr show ex200a > output/runtime.txt
ping -c 2 10.66.8.254 > output/ping4.txt
ping -6 -c 2 fd00:66:8::fe > output/ping6.txt
getent hosts peer-net > output/getent.txt
EOS
