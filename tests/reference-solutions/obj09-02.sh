#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj09-02
sudo grubby --update-kernel=ALL --args="systemd.show_status=1"
sudo grubby --info=ALL > output/grubby.txt
EOS
