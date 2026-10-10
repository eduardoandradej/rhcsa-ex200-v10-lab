#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj10-01
getenforce > output/getenforce.txt
sestatus > output/sestatus.txt
ps -eZ | grep '[s]shd' > output/sshd-process.txt
ls -Z /etc/ssh/sshd_config > output/sshd-config.txt
sudo semanage fcontext -l -C > output/fcontext-local.txt
EOS
