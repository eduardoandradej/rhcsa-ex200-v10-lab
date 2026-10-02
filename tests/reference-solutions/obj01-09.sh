#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -s' <<'EOS'
cd /home/student/rhcsa-lab/obj01-09
man -w chmod > output/chmod-manpath.txt
printf '1\n' > output/chmod-section.txt
printf '5\n' > output/passwd-section.txt
rpm -qd openssh-clients | grep -E '/ssh\.1(\.gz)?$' > output/ssh-manpage.txt
printf '%s\n' '-c' > output/tar-create-option.txt
EOS
