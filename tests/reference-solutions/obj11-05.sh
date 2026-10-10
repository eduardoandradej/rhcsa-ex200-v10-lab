#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj11-05
echo 'serverb:/srv/rhcsa11/systemd /mnt/rhcsa11-auto nfs rw,sync,x-systemd.automount 0 0' | sudo tee -a /etc/fstab >/dev/null
sudo systemctl daemon-reload
UNIT=$(systemd-escape --path --suffix=automount /mnt/rhcsa11-auto)
sudo systemctl start "$UNIT"
systemctl is-active "$UNIT" > output/unit.txt
cat /mnt/rhcsa11-auto/hello.txt > output/content.txt
findmnt -T /mnt/rhcsa11-auto/hello.txt > output/findmnt.txt
EOS
