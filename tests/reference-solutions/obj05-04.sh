#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj05-04
cpid=$(cat /run/rhcsa-cpu-hog.pid)
mpid=$(cat /run/rhcsa-mem-hog.pid)
ps -o pid=,%cpu=,%mem=,stat=,args= -p "$cpid" > output/cpu-before.txt
ps -o pid=,%cpu=,%mem=,stat=,args= -p "$mpid" > output/memory-before.txt
kill -s TERM "$cpid"
kill -s TERM "$mpid"
for _ in {1..30}; do
  if [[ ! -e /proc/$cpid && ! -e /proc/$mpid ]]; then
    break
  fi
  sleep 0.1
done
EOS
