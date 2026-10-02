# RHCSA EX200 v10 Lab — Roadmap

## Estado atual

| Objective | Tema | Labs |
|---|---|---:|
| 01 | Essential Tools | 10 — concluído |
| 02 | Users & Groups | 8 — concluído |
| 03 | RPM, DNF & Repositories | 8 — concluído |
| 04 | Simple Shell Scripts | 8 — concluído |
| 05 | Processes, Scheduling, Tuning & systemd | 10 — implementação v1.1.0 |

Total após esta entrega: **44 labs**.

## Próximos blocos

| Objective | Tema | Labs estimados |
|---|---|---:|
| 06 | Networking / NetworkManager | 8 |
| 07 | Scheduling, logs e chrony | 8 |
| 08 | Storage, swap e LVM | 12 |
| 09 | Boot, GRUB e recuperação | 7 |
| 10 | SELinux e firewalld | 9 |
| 11 | NFS e autofs | 6 |
| 12 | Simulados integrados EX200 | 6 |

> A estimativa original de 9 labs para OBJ05 foi ampliada para 10 para
> manter separado o treinamento de job control, sinais, nice/renice,
> TuneD e os três níveis de gerenciamento systemd.

## Quality gate

Each ready lab includes:

- setup;
- PT-BR and EN prompts;
- behavior/state grader;
- finish/cleanup;
- reference solution;
- automated reference solver.

The release gate validates Python, shell syntax, YAML contracts, grader
`--json`, Ansible syntax, and CLI smoke.
