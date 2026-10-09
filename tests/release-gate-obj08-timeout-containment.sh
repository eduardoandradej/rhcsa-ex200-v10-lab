#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== OBJ08 timeout containment contract =="

runner="$ROOT/labctl/runner.py"
setup09="$ROOT/labs/08-storage/09-lvextend-xfs/setup.yml"
setup10="$ROOT/labs/08-storage/10-vgextend/setup.yml"
reset="$ROOT/ansible/files/rhcsa-storage-reset"

grep -q 'start_new_session=True' "$runner" || {
  echo "FAIL: runner does not isolate ansible into its own process group."
  exit 1
}
grep -q 'os.killpg(proc.pid, signal.SIGTERM)' "$runner" || {
  echo "FAIL: runner timeout does not terminate the ansible/ssh process group."
  exit 1
}
grep -q 'os.killpg(proc.pid, signal.SIGKILL)' "$runner" || {
  echo "FAIL: runner timeout has no SIGKILL fallback."
  exit 1
}
grep -q 'returncode=124' "$runner" || {
  echo "FAIL: runner timeout does not return controlled status 124."
  exit 1
}

for setup in "$setup09" "$setup10"; do
  grep -q -- '--kill-after=2s' "$setup" || {
    echo "FAIL: $(basename "$(dirname "$setup")") lacks remote command timeout."
    exit 1
  }
  grep -q '30s' "$setup" || {
    echo "FAIL: $(basename "$(dirname "$setup")") lacks bounded 30s commands."
    exit 1
  }
done

grep -q 'local rc=0' "$reset" || {
  echo "FAIL: reset does not capture return codes safely."
  exit 1
}
grep -q '"\$@" || rc=\$?' "$reset" || {
  echo "FAIL: reset can still report false rc=0 after timeout."
  exit 1
}

bad="$(
  grep -RPsn \
    'sudo (pvcreate|vgcreate|vgextend|lvcreate|lvextend|mkfs\.xfs|mkswap|mount|xfs_growfs)\b' \
    "$ROOT/tests/reference-solutions" --include='obj08-*.sh' 2>/dev/null |
  grep -v 'sudo timeout ' || true
)"
if [[ -n "$bad" ]]; then
  echo "$bad"
  echo "FAIL: unbounded destructive/LVM reference command remains."
  exit 1
fi

echo "OK: local ansible/ssh process groups and remote storage commands are bounded"
