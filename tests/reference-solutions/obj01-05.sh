#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -s' <<'EOS'
cd /home/student/rhcsa-lab/obj01-05
tar -cf output/project.tar project
gzip -c output/project.tar > output/project.tar.gz
bzip2 -c output/project.tar > output/project.tar.bz2
tar -xzf output/project.tar.gz -C restore-gzip
tar -xjf output/project.tar.bz2 -C restore-bzip2
EOS
