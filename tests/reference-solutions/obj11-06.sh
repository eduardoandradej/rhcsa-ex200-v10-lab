#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj11-06
sudo mount -t nfs -o rw,sync serverb:/srv/rhcsa11/integrated /mnt/rhcsa11-check
findmnt /mnt/rhcsa11-check > output/manual.txt
ls -l /mnt/rhcsa11-check > output/list.txt
sudo umount /mnt/rhcsa11-check
echo '/remote11-final /etc/auto.rhcsa11' | sudo tee /etc/auto.master.d/rhcsa11.autofs >/dev/null
echo '* -rw,sync,fstype=nfs serverb:/srv/rhcsa11/integrated/&' | sudo tee /etc/auto.rhcsa11 >/dev/null
sudo systemctl enable --now autofs
{ cat /remote11-final/red/info.txt; cat /remote11-final/hat/info.txt; } > output/content.txt
{ findmnt -T /remote11-final/red/info.txt; findmnt -T /remote11-final/hat/info.txt; } > output/findmnt.txt
EOS
