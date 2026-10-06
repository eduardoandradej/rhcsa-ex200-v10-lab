#!/usr/bin/env bash
set -Eeuo pipefail

ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj07-02

echo 'd /run/rhcsa-momentary 0700 root root 30s' | \
  sudo tee /etc/tmpfiles.d/rhcsa-momentary.conf >/dev/null

sudo systemd-tmpfiles --create /etc/tmpfiles.d/rhcsa-momentary.conf
sudo touch /run/rhcsa-momentary/stale.txt

# Let the file actually age beyond the 30-second cleanup threshold.
sleep 35

sudo systemd-tmpfiles --clean /etc/tmpfiles.d/rhcsa-momentary.conf

stat -c '%a %U %G %n' /run/rhcsa-momentary > output/stat.txt
EOS
