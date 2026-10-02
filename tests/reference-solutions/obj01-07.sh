#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -s' <<'EOS'
cd /home/student/rhcsa-lab/obj01-07
ln data/inventory.txt links/inventory.hard
ln -s ../data/app.conf links/current.conf
ln -s ../data/docs links/docs
EOS
