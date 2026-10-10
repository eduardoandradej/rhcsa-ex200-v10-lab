#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj10-07
sudo semanage port -a -t http_port_t -p tcp 48888
sudo systemctl start httpd
sudo semanage port -l -C > output/ports.txt
sudo ss -ltnp | grep ':48888 ' > output/listen.txt
EOS
