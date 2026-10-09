#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj08-03
sudo timeout --signal=TERM --kill-after=2s 30s mkfs.xfs -f -L RHCSA08XFS /dev/vdb1
sudo timeout --signal=TERM --kill-after=2s 30s mount /dev/vdb1 /mnt/rhcsa-xfs
echo OBJ08-XFS | sudo tee /mnt/rhcsa-xfs/obj08.txt >/dev/null
findmnt /mnt/rhcsa-xfs > output/findmnt.txt
lsblk -f /dev/vdb > output/lsblk.txt
EOS
