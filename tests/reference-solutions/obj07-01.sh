#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj07-01
sudo cp /usr/lib/systemd/system/sysstat-collect.timer /etc/systemd/system/sysstat-collect.timer
sudo sed -i 's#OnCalendar=.*#OnCalendar=*:00/2#' /etc/systemd/system/sysstat-collect.timer
sudo systemctl daemon-reload
sudo systemctl enable --now sysstat-collect.timer
systemctl cat sysstat-collect.timer > output/timer.txt
systemctl list-timers sysstat-collect.timer --all --no-pager > output/list-timers.txt
EOS
