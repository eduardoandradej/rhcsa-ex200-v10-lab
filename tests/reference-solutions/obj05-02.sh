#!/usr/bin/env bash
set -Eeuo pipefail

# First SSH session: exercise real Bash job control and capture evidence.
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj05-02
set -m

nohup ./assets/job-alpha >/dev/null 2>&1 &
alpha=$!
echo "$alpha" > output/alpha.pid

nohup ./assets/job-beta >/dev/null 2>&1 &
beta=$!
echo "$beta" > output/beta.pid

# Avoid a race: wait until nohup/script have exec()'d the final processes.
for _ in {1..100}; do
    a_args="$(ps -o args= -p "$alpha" 2>/dev/null || true)"
    b_args="$(ps -o args= -p "$beta" 2>/dev/null || true)"
    [[ "$a_args" == rhcsa-job-alpha* && "$b_args" == rhcsa-job-beta* ]] && break
    sleep 0.02
done

[[ "$(ps -o args= -p "$alpha" 2>/dev/null || true)" == rhcsa-job-alpha* ]]
[[ "$(ps -o args= -p "$beta" 2>/dev/null || true)" == rhcsa-job-beta* ]]

kill -s STOP %1

for _ in {1..50}; do
    state="$(ps -o stat= -p "$alpha" 2>/dev/null || true)"
    [[ "$state" == *T* ]] && break
    sleep 0.02
done

jobs -l > output/jobs.txt
ps -o pid=,stat=,args= -p "$alpha,$beta" > output/processes.txt

# A stopped process group is automatically continued when its controlling
# shell exits and the process group becomes orphaned. Therefore detach while
# both jobs are running; final STOP is applied from a second SSH session.
kill -s CONT %1
disown %1 %2
EOS

# Second SSH session: establish the final graded state after the first shell
# (and its job-control process group) no longer exists.
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
alpha="$(cat /home/student/rhcsa-lab/obj05-02/output/alpha.pid)"
/usr/bin/kill -s STOP "$alpha"

for _ in {1..50}; do
    state="$(ps -o stat= -p "$alpha" 2>/dev/null || true)"
    [[ "$state" == *T* ]] && exit 0
    sleep 0.02
done

echo "alpha did not reach stopped state" >&2
exit 1
EOS
