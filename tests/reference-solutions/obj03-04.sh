#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'sudo bash -Eeuo pipefail -s' <<'EOS'
dnf -y install rhcsa-toolkit
dnf -y install rhcsa-temp
rpm -q rhcsa-toolkit rhcsa-temp
dnf -y remove rhcsa-temp
EOS
