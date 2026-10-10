#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj10-03
sudo semanage fcontext -a -t httpd_sys_content_t '/srv/web10(/.*)?'
sudo restorecon -Rv /srv/web10
{ ls -Zd /srv/web10; ls -Z /srv/web10/index.html; } > output/contexts.txt
sudo semanage fcontext -l -C | grep '/srv/web10' > output/fcontext.txt
EOS
