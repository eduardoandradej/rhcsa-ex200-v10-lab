#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj03-07
sudo dnf -y install rhcsa-history
dnf history list rhcsa-history > output/history-after-install.txt
sudo dnf -y remove rhcsa-history
dnf history list rhcsa-history > output/history-after-remove.txt
id="$(dnf history list rhcsa-history | awk '$1 ~ /^[0-9]+$/ {print $1; exit}')"
dnf history info "$id" > output/last-transaction.txt
EOS
