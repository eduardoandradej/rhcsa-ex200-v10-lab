#!/usr/bin/env bash
set -Eeuo pipefail

ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj05-05

nohup nice -n 12 ./assets/nice-start >/dev/null 2>&1 &
p1=$!
echo "$p1" > output/nice-start.pid

nohup ./assets/nice-change >/dev/null 2>&1 &
p2=$!
echo "$p2" > output/nice-change.pid

for _ in {1..100}; do
    a1="$(ps -o args= -p "$p1" 2>/dev/null || true)"
    a2="$(ps -o args= -p "$p2" 2>/dev/null || true)"
    [[ "$a1" == rhcsa-nice-start* && "$a2" == rhcsa-nice-change* ]] && break
    sleep 0.02
done

[[ "$(ps -o args= -p "$p1" 2>/dev/null || true)" == rhcsa-nice-start* ]]
[[ "$(ps -o args= -p "$p2" 2>/dev/null || true)" == rhcsa-nice-change* ]]

renice -n 7 -p "$p2" >/dev/null
ps -o pid=,ni=,stat=,args= -p "$p1,$p2" > output/priorities.txt
disown -a 2>/dev/null || true
EOS
