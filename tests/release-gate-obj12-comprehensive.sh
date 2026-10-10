#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== OBJ12 comprehensive challenge contract =="

mapfile -t labs < <(find "$ROOT/labs/12-comprehensive" -mindepth 2 -maxdepth 2 -name lab.yml | sort)
[[ "${#labs[@]}" -eq 6 ]] || {
  echo "FAIL: expected 6 OBJ12 labs, got ${#labs[@]}"
  exit 1
}

for f in "${labs[@]}"; do
  grep -q '^status: ready$' "$f" || {
    echo "FAIL: all OBJ12 labs must be runtime-gradeable"
    exit 1
  }
  grep -q '^difficulty: 5$' "$f" || {
    echo "FAIL: OBJ12 final challenges must remain difficulty 5"
    exit 1
  }
done

# Final challenges must not weaken the host to make grading easier.
if grep -RIEq 'SELINUX=disabled|selinux=0|setenforce[[:space:]]+0|audit2allow|no_root_squash' \
  "$ROOT/labs/12-comprehensive" \
  "$ROOT/tests/reference-solutions"/obj12-*.sh; then
  echo "FAIL: OBJ12 contains a forbidden security shortcut"
  exit 1
fi

# No reboot/shutdown in the automated comprehensive path.
if grep -RIEq '(^|[[:space:]])(reboot|shutdown|poweroff|init[[:space:]]+6)([[:space:]]|$)' \
  "$ROOT/tests/reference-solutions"/obj12-*.sh; then
  echo "FAIL: OBJ12 automated solvers may not reboot the VM"
  exit 1
fi

# Storage challenge is restricted to the scratch disk.
storage="$ROOT/labs/12-comprehensive/03-storage-lvm-swap"
grep -Rqs 'rhcsa-storage-guard.*blank.*vdb' "$storage/setup.yml" || {
  echo "FAIL: OBJ12 storage setup must guard /dev/vdb"
  exit 1
}
grep -Rqs 'rhcsa-storage-reset.*vdb' "$storage/finish.yml" || {
  echo "FAIL: OBJ12 storage finish must reset /dev/vdb"
  exit 1
}
if grep -RIEq '/dev/vda' "$storage" "$ROOT/tests/reference-solutions/obj12-03.sh"; then
  echo "FAIL: OBJ12 storage may not reference protected /dev/vda"
  exit 1
fi

# Fstab-changing labs must back up and restore fstab.
for id in 03-storage-lvm-swap 04-boot-maintenance; do
  setup="$ROOT/labs/12-comprehensive/$id/setup.yml"
  finish="$ROOT/labs/12-comprehensive/$id/finish.yml"
  grep -q 'src: /etc/fstab' "$setup" || {
    echo "FAIL: $id setup must back up /etc/fstab"
    exit 1
  }
  grep -q 'dest: /etc/fstab' "$finish" || {
    echo "FAIL: $id finish must restore /etc/fstab"
    exit 1
  }
done

# Reference solvers use stdin to feed remote bash.
for solver in "$ROOT"/tests/reference-solutions/obj12-*.sh; do
  grep -q '^set -Eeuo pipefail$' "$solver" || {
    echo "FAIL: ${solver#"$ROOT"/} must use strict shell mode"
    exit 1
  }
  if grep -Eq "ssh[[:space:]]+-n[[:space:]]+servera.*<<['\"]?EOS['\"]?" "$solver"; then
    echo "FAIL: ${solver#"$ROOT"/} combines ssh -n with a here-document"
    exit 1
  fi
done

# Coverage checks for the final six.
grep -Rqs 'setfacl' "$ROOT/tests/reference-solutions/obj12-01.sh" || { echo "FAIL: OBJ12-01 must cover ACL"; exit 1; }
grep -Rqs 'systemd-tmpfiles' "$ROOT/tests/reference-solutions/obj12-02.sh" || { echo "FAIL: OBJ12-02 must cover tmpfiles"; exit 1; }
grep -Rqs 'vgcreate vg12' "$ROOT/tests/reference-solutions/obj12-03.sh" || { echo "FAIL: OBJ12-03 must cover LVM"; exit 1; }
grep -Rqs 'grubby --update-kernel=ALL' "$ROOT/tests/reference-solutions/obj12-04.sh" || { echo "FAIL: OBJ12-04 must cover persistent kernel arguments"; exit 1; }
grep -Rqs 'semanage port' "$ROOT/tests/reference-solutions/obj12-05.sh" || { echo "FAIL: OBJ12-05 must cover SELinux port labeling"; exit 1; }
grep -Rqs 'serverb:/srv/rhcsa11/integrated/&' "$ROOT/tests/reference-solutions/obj12-06.sh" || { echo "FAIL: OBJ12-06 must cover indirect NFS AutoFS"; exit 1; }

echo "OK: 6 final challenges cover the integrated RHCSA skill set with safe cleanup boundaries"
# Graders must not directly read privileged log files as the student account.
ops_grader="$ROOT/labs/12-comprehensive/02-operations-services/grade.py"
if grep -Fq 'Path("/var/log/ops12.log").read_text' "$ops_grader"; then
  echo "FAIL: obj12-02 grader directly reads privileged /var/log/ops12.log"
  exit 1
fi
grep -Fq 'run(["sudo","-n","cat","/var/log/ops12.log"])' "$ops_grader" || {
  echo "FAIL: obj12-02 grader must read the privileged log through sudo -n"
  exit 1
}

echo "OK: obj12-02 grader reads the rsyslog output through the privileged execution path"
