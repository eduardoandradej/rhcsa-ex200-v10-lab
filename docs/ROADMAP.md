# RHCSA EX200 v10 Lab — Roadmap

## Estado atual

| Objective | Tema | Labs / itens |
|---|---|---:|
| 01 | Essential Tools | 10 — concluído |
| 02 | Users & Groups | 8 — concluído |
| 03 | RPM, DNF & Repositories | 8 — concluído |
| 04 | Simple Shell Scripts | 8 — concluído |
| 05 | Processes, Scheduling, Tuning & systemd | 10 — concluído |
| 06 | Networking / NetworkManager | 8 — concluído |
| 07 | Scheduling, Temporary Files, Logging & Time | 8 — concluído |
| 08 | Partitions, Filesystems, Swap & LVM | 12 — concluído |
| 09 | Boot, GRUB & Recovery | 7 — v1.5.0 |

OBJ09 has **5 automated/runtime-gradeable labs** and **2 manual console
drills** (`obj09-04` and `obj09-06`).

Totals after v1.5.0:

- automated runtime-gradeable labs: **77**;
- curriculum items including manual console drills: **79**.

## Próximos blocos

| Objective | Tema | Labs estimados |
|---|---|---:|
| 10 | SELinux e firewalld | 9 |
| 11 | NFS e autofs | 6 |
| 12 | Simulados integrados EX200 | 6 |

## Quality gate

Every `ready` lab includes setup, PT-BR and EN prompts, behavior/state grader,
finish/cleanup, reference solution, and automated reference solver.

Manual console entries are explicitly marked `manual-only` and are excluded
from automated reference integration. The release gate verifies this boundary.

The release gate also validates Python, shell syntax, YAML contracts, grader
`--json`, Ansible syntax on the lab host, and CLI smoke.
