#!/usr/bin/env bash
set -Eeuo pipefail

ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj05-06

tuned-adm recommend > output/recommended.txt
tuned-adm list > output/profiles.txt

sudo tuned-adm profile throughput-performance

tuned-adm active > output/active.txt

# tuned-adm verify is diagnostic. Preserve both its output and exit status,
# but do not abort the reference solution solely because verify reports a
# host/profile deviation.
set +e
sudo tuned-adm verify > output/verify.txt 2>&1
verify_rc=$?
set -e

printf '%s\n' "$verify_rc" > output/verify.rc

# The graded final state is the selected active profile.
grep -q 'throughput-performance' output/active.txt
EOS
