# OBJ08 — Storage Safety Contract

OBJ08 is intentionally destructive on **scratch disks only**.

## Protected system storage

The following are never authorized as training targets:

- `/dev/vda`
- `/dev/vda1`
- `/dev/vda2`
- `rhel_servera/root`
- `rhel_servera/swap`

## Authorized servera scratch disks

- `/dev/vdb` — 5 GiB
- `/dev/vdc` — 5 GiB
- `/dev/vdd` — 3 GiB
- `/dev/vde` — 2 GiB

The preflight validates host identity, block-device type, and expected size
range before a destructive lab starts.

## Snapshot recovery proof

The servera baseline snapshot was manually proven before OBJ08 by creating a
marker after the snapshot, reverting to `rhcsa-baseline-v0.7.2`, and confirming
that the marker disappeared while the original root/swap layout returned.

Normal `lab finish` uses a guarded reset limited to the scratch allowlist.
Snapshot revert remains the out-of-band recovery path for abnormal failures.

## fstab safety

Every destructive lab saves `/etc/fstab` before student work and restores the
saved copy during `lab finish`. Persistent-mount labs require validation with
`findmnt --verify`.

## QA-only reference solvers

Reference solutions exist to validate lab/grader contracts. Student practice
should be performed manually from the prompt before inspecting solutions.
