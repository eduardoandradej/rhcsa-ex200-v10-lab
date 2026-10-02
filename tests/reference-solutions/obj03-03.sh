#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj03-03
dnf search toolkit > output/search.txt
dnf info rhcsa-toolkit > output/info.txt
dnf provides /usr/local/share/rhcsa-toolkit/version.txt > output/provider.txt
dnf list rhcsa-toolkit > output/list.txt
EOS
