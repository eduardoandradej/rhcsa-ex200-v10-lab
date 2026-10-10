#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj11-04
echo '/remote11 /etc/auto.rhcsa11' | sudo tee /etc/auto.master.d/rhcsa11.autofs >/dev/null
echo '* -rw,sync,fstype=nfs serverb:/srv/rhcsa11/projects/&' | sudo tee /etc/auto.rhcsa11 >/dev/null
sudo systemctl enable --now autofs
{ cat /remote11/alpha/info.txt; cat /remote11/beta/info.txt; } > output/content.txt
{ findmnt -T /remote11/alpha/info.txt; findmnt -T /remote11/beta/info.txt; } > output/findmnt.txt
EOS
