#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj08-09
sudo timeout --signal=TERM --kill-after=2s 30s lvextend -L 2G /dev/rhcsa_vgdata/rhcsa_lvdata >/dev/null
sudo timeout --signal=TERM --kill-after=2s 30s xfs_growfs /lvextend >/dev/null
sudo lvs > output/lvs.txt
df -h /lvextend > output/df.txt
sudo xfs_info /lvextend > output/xfs-info.txt
EOS
