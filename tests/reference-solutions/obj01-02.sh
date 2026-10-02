#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -s' <<'EOS'
cd /home/student/rhcsa-lab/obj01-02
bin/stream-demo > output/stdout.log 2> output/stderr.log
bin/stream-demo > output/combined.log 2>&1
bin/append-demo >> output/append.log
bin/append-demo >> output/append.log
sort input/services.txt | uniq > output/services-unique.txt
grep -w 'active' input/status.txt | wc -l > output/active-count.txt
EOS
