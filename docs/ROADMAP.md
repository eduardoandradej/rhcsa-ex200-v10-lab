# RHCSA EX200 v10 Lab — Roadmap

## Estado atual

| Objective | Tema | Labs |
|---|---|---:|
| 01 | Essential Tools | 10 — concluído |
| 02 | Users & Groups | 8 — concluído |
| 03 | RPM, DNF & Repositories | 8 — concluído |
| 04 | Simple Shell Scripts | 8 — implementação v1.0.0 |

Total após esta entrega: **34 labs**.

## Próximos blocos

| Objective | Tema | Labs estimados |
|---|---|---:|
| 05 | Processos e serviços systemd | 9 |
| 06 | Networking / NetworkManager | 8 |
| 07 | Scheduling, logs e chrony | 8 |
| 08 | Storage, swap e LVM | 12 |
| 09 | Boot, GRUB e recuperação | 7 |
| 10 | SELinux e firewalld | 9 |
| 11 | NFS e autofs | 6 |
| 12 | Simulados integrados EX200 | 6 |

## Critério de qualidade

Cada laboratório `ready` inclui:

- preparação idempotente;
- enunciado PT-BR e EN;
- grader por estado/comportamento;
- limpeza;
- solução de referência;
- solver de regressão automatizado.

A release gate valida Python, YAML, Ansible, contrato `--json`, sintaxe dos
reference solvers e smoke da CLI.
