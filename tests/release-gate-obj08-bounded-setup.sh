#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== OBJ08 bounded storage setup contract =="

for folder in 09-lvextend-xfs 10-vgextend; do
  setup="$ROOT/labs/08-storage/$folder/setup.yml"

  if grep -Eq '^[[:space:]]+udevadm settle[[:space:]]*$' "$setup"; then
    echo "FAIL: $folder still contains an unbounded udevadm settle."
    exit 1
  fi

  grep -q 'ansible.builtin.wait_for:' "$setup" || {
    echo "FAIL: $folder does not use a bounded device-node wait."
    exit 1
  }

  grep -q 'timeout: 15' "$setup" || {
    echo "FAIL: $folder device-node wait has no 15-second bound."
    exit 1
  }
done

# obj08-09 must expose each destructive preparation stage as its own task,
# so a future failure identifies PV/VG/LV/XFS/mount rather than timing out in
# one opaque shell task.
setup="$ROOT/labs/08-storage/09-lvextend-xfs/setup.yml"
for task in \
  "Create PV on vdc1" \
  "Create rhcsa_vgdata VG" \
  "Create 1 GiB rhcsa_lvdata LV" \
  "Create XFS filesystem" \
  "Mount prepared XFS filesystem"
do
  grep -q "$task" "$setup" || {
    echo "FAIL: obj08-09 missing granular task: $task"
    exit 1
  }
done

echo "OK: obj08-09/10 preparation is bounded and diagnostically granular"
