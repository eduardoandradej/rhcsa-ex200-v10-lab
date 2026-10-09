#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj08-01
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,UUID > output/lsblk.txt
sudo blkid > output/blkid.txt
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdb print > output/parted-vdb.txt 2>&1 || true
sudo pvs > output/pvs.txt
sudo vgs > output/vgs.txt
sudo lvs > output/lvs.txt
findmnt > output/findmnt.txt
EOS
