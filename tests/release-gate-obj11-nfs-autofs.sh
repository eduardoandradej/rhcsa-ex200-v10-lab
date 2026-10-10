#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== OBJ11 NFS/AutoFS safety and coverage =="

mapfile -t labs < <(find "$ROOT/labs/11-nfs-autofs" -mindepth 2 -maxdepth 2 -name lab.yml | sort)
[[ "${#labs[@]}" -eq 6 ]] || {
  echo "FAIL: expected 6 OBJ11 labs, got ${#labs[@]}"
  exit 1
}

for f in "${labs[@]}"; do
  grep -q '^status: ready$' "$f" || {
    echo "FAIL: every OBJ11 lab must be runtime-gradeable"
    exit 1
  }
done

# Dedicated training infrastructure only.
grep -q '/srv/rhcsa11' "$ROOT/ansible/prepare-objective11.yml" || {
  echo "FAIL: OBJ11 NFS provider must use the dedicated /srv/rhcsa11 tree"
  exit 1
}

if grep -RIEq 'no_root_squash|/dev/vda|mkfs|pvcreate|vgcreate|lvcreate' \
  "$ROOT/ansible/prepare-objective11.yml" \
  "$ROOT/labs/11-nfs-autofs" \
  "$ROOT/tests/reference-solutions"/obj11-*.sh; then
  echo "FAIL: OBJ11 may not weaken NFS root squashing or touch block storage"
  exit 1
fi

# Client fstab exercises must have a setup backup and finish restore.
for id in 02-persistent-nfs-fstab 05-systemd-automount; do
  setup="$ROOT/labs/11-nfs-autofs/$id/setup.yml"
  finish="$ROOT/labs/11-nfs-autofs/$id/finish.yml"
  grep -q 'src: /etc/fstab' "$setup" || {
    echo "FAIL: $id setup must back up /etc/fstab"
    exit 1
  }
  grep -q 'dest: /etc/fstab' "$finish" || {
    echo "FAIL: $id finish must restore /etc/fstab"
    exit 1
  }
done

grep -Rqs 'mount -t nfs' "$ROOT/tests/reference-solutions"/obj11-*.sh || {
  echo "FAIL: OBJ11 must cover manual NFS mounting"
  exit 1
}
grep -Rqs 'rw,sync' "$ROOT/tests/reference-solutions"/obj11-*.sh || {
  echo "FAIL: OBJ11 must cover rw,sync mount options"
  exit 1
}
grep -Rqs '/- /etc/auto.rhcsa11' "$ROOT/tests/reference-solutions"/obj11-*.sh || {
  echo "FAIL: OBJ11 must cover a direct AutoFS map"
  exit 1
}
grep -Rqs 'serverb:/srv/rhcsa11/projects/&' "$ROOT/tests/reference-solutions"/obj11-*.sh || {
  echo "FAIL: OBJ11 must cover indirect wildcard maps"
  exit 1
}
grep -Rqs 'x-systemd.automount' "$ROOT/tests/reference-solutions"/obj11-*.sh || {
  echo "FAIL: OBJ11 must cover systemd automount from fstab"
  exit 1
}

# Reference solvers feed remote scripts through stdin.
for solver in "$ROOT"/tests/reference-solutions/obj11-*.sh; do
  if grep -Eq "ssh[[:space:]]+-n[[:space:]]+servera.*<<['\"]?EOS['\"]?" "$solver"; then
    echo "FAIL: ${solver#"$ROOT"/} combines ssh -n with a here-document"
    exit 1
  fi
done

echo "OK: 6 labs cover manual NFS, fstab persistence, direct/indirect AutoFS, and systemd automount"
