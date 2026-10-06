#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj07-03
sudo tee /etc/cron.d/rhcsa-report >/dev/null <<'EOF'
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root
*/5 * * * * student /usr/bin/id -un >> /home/student/rhcsa-lab/obj07-03/cron-run.txt
EOF
sudo chmod 0644 /etc/cron.d/rhcsa-report
sudo cat /etc/cron.d/rhcsa-report > output/cron.txt
EOS
