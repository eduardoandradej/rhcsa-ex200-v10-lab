#!/usr/bin/env bash
set -Eeuo pipefail

ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj10-05

sudo ausearch -if input/avc.audit -m AVC > output/avc.txt

sudo semanage fcontext -a -t httpd_sys_content_t '/srv/avc10(/.*)?'
sudo restorecon -Rv /srv/avc10

ls -Zd /srv/avc10 /srv/avc10/index.html > output/context.txt
curl -sS http://127.0.0.1/avc10/index.html > output/curl.txt
EOS
