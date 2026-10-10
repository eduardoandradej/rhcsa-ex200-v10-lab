#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== OBJ09 scope and safety contract =="

mapfile -t labs < <(find "$ROOT/labs/09-boot-recovery" -mindepth 2 -maxdepth 2 -name lab.yml | sort)
[[ "${#labs[@]}" -eq 7 ]] || {
  echo "FAIL: expected 7 OBJ09 catalog entries, got ${#labs[@]}"
  exit 1
}

for id in obj09-01 obj09-02 obj09-03 obj09-05 obj09-07; do
  f="$(grep -Rl "^id: $id$" "$ROOT/labs/09-boot-recovery"/*/lab.yml)"
  grep -q '^status: ready$' "$f" || {
    echo "FAIL: $id must be ready"
    exit 1
  }
done

for id in obj09-04 obj09-06; do
  f="$(grep -Rl "^id: $id$" "$ROOT/labs/09-boot-recovery"/*/lab.yml)"
  grep -q '^status: manual-only$' "$f" || {
    echo "FAIL: $id must remain manual-only"
    exit 1
  }
done

# Automated setup/reference paths must never reboot the VM or invoke interactive
# boot-loader recovery. Manual console drills are intentionally kept outside
# this search.
auto_paths=(
  "$ROOT/labs/09-boot-recovery/01-boot-inventory/setup.yml"
  "$ROOT/labs/09-boot-recovery/01-boot-inventory/finish.yml"
  "$ROOT/labs/09-boot-recovery/02-grubby-kernel-args/setup.yml"
  "$ROOT/labs/09-boot-recovery/02-grubby-kernel-args/finish.yml"
  "$ROOT/labs/09-boot-recovery/03-default-target/setup.yml"
  "$ROOT/labs/09-boot-recovery/03-default-target/finish.yml"
  "$ROOT/labs/09-boot-recovery/05-fstab-recovery/setup.yml"
  "$ROOT/labs/09-boot-recovery/05-fstab-recovery/finish.yml"
  "$ROOT/labs/09-boot-recovery/07-integrated-challenge/setup.yml"
  "$ROOT/labs/09-boot-recovery/07-integrated-challenge/finish.yml"
  "$ROOT/tests/reference-solutions/obj09-01.sh"
  "$ROOT/tests/reference-solutions/obj09-02.sh"
  "$ROOT/tests/reference-solutions/obj09-03.sh"
  "$ROOT/tests/reference-solutions/obj09-05.sh"
  "$ROOT/tests/reference-solutions/obj09-07.sh"
)

if grep -IEq \
  'systemctl[[:space:]]+reboot|(^|[[:space:]])reboot([[:space:]]|$)|shutdown[[:space:]]|init=/bin/bash|systemd\.unit=(emergency|rescue)\.target' \
  "${auto_paths[@]}"; then
  echo "FAIL: automated OBJ09 path contains reboot or interactive recovery action"
  exit 1
fi

if grep -Rqs '/dev/vda' "$ROOT/labs/09-boot-recovery"; then
  echo "FAIL: OBJ09 lab content must not target /dev/vda"
  exit 1
fi

grep -q 'rhcsa-storage-guard' \
  "$ROOT/labs/09-boot-recovery/05-fstab-recovery/setup.yml" || {
  echo "FAIL: obj09-05 must use the storage guard"
  exit 1
}

grep -q 'nofail' "$ROOT/labs/09-boot-recovery/05-fstab-recovery/setup.yml" || {
  echo "FAIL: obj09-05 initial fstab state must remain boot-safe"
  exit 1
}

if grep -Eq 'obj09-04|obj09-06' "$ROOT/tests/integration-objective09.sh"; then
  # They may only be mentioned in the explanatory note, never as integration args.
  line="$(grep 'integration-reference.sh' -A2 "$ROOT/tests/integration-objective09.sh" | tr '\n' ' ')"
  if grep -Eq 'obj09-04|obj09-06' <<<"$line"; then
    echo "FAIL: manual console labs entered automated integration"
    exit 1
  fi
fi


# `ssh -n` redirects stdin from /dev/null. Combining it with a here-document
# makes the remote `bash -s` receive no solution body while SSH still exits 0.
for solver in "$ROOT"/tests/reference-solutions/obj09-*.sh; do
  [[ -f "$solver" ]] || continue
  if grep -Eq "ssh[[:space:]]+-n[[:space:]]+servera.*<<['\"]?EOS['\"]?" "$solver"; then
    echo "FAIL: ${solver#"$ROOT"/} combines ssh -n with a here-document."
    exit 1
  fi
done

echo "OK: 5 automated labs + 2 manual-console drills with safe boundary"
