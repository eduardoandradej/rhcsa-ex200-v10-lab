#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj07-05
journalctl -t obj07-journal --since '-10 min' --no-pager > output/tag.txt
journalctl -t obj07-journal -p warning --since '-10 min' --no-pager > output/warning.txt
journalctl _SYSTEMD_UNIT=rhcsa-journal.service --no-pager > output/unit.txt
EOS
