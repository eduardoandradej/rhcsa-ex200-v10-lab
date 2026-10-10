#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj11-01
showmount --exports serverb > output/exports.txt
sudo mount -t nfs -o rw,sync serverb:/srv/rhcsa11/manual /mnt/rhcsa11-manual
findmnt /mnt/rhcsa11-manual > output/mount.txt
cat /mnt/rhcsa11-manual/hello.txt > output/content.txt
sudo umount /mnt/rhcsa11-manual
if findmnt /mnt/rhcsa11-manual >/dev/null 2>&1; then echo mounted > output/unmounted.txt; else echo unmounted > output/unmounted.txt; fi
EOS
