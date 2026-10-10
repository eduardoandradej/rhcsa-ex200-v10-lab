#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj10-06
sudo firewall-cmd --permanent --zone=rhcsa10 --add-source=198.51.100.0/24
sudo firewall-cmd --permanent --zone=rhcsa10 --add-service=http
sudo firewall-cmd --permanent --zone=rhcsa10 --add-port=45100/tcp
sudo firewall-cmd --reload
sudo firewall-cmd --zone=rhcsa10 --list-all > output/runtime.txt
sudo firewall-cmd --permanent --zone=rhcsa10 --list-all > output/permanent.txt
EOS
