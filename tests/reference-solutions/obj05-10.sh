#!/usr/bin/env bash
set -Eeuo pipefail

ssh serverb 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj05-10

rogue=$(cat /run/rhcsa-rogue-cpu.pid)
ps -o pid=,%cpu=,%mem=,ni=,stat=,args= -p "$rogue" > output/rogue-before.txt

kill -s TERM "$rogue"
for _ in {1..30}; do
    [[ ! -e /proc/$rogue ]] && break
    sleep 0.1
done

nohup nice -n 10 ./assets/batch-worker >/dev/null 2>&1 &
batch=$!
echo "$batch" > output/batch.pid

for _ in {1..100}; do
    args="$(ps -o args= -p "$batch" 2>/dev/null || true)"
    [[ "$args" == rhcsa-batch-worker* ]] && break
    sleep 0.02
done
[[ "$(ps -o args= -p "$batch" 2>/dev/null || true)" == rhcsa-batch-worker* ]]
disown -a 2>/dev/null || true

sudo systemctl enable --now rhcsa-api.service
sudo systemctl stop rhcsa-legacy.service
sudo systemctl disable rhcsa-legacy.service
sudo systemctl mask rhcsa-legacy.service

sudo tuned-adm profile balanced
tuned-adm active > output/tuned-active.txt
EOS
