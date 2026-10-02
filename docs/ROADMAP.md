# RHCSA EX200 v10 Lab — Roadmap

## Estado atual

| Objective | Tema | Labs |
|---|---|---:|
| 01 | Essential Tools | 10 — concluído |
| 02 | Users & Groups | 8 — concluído |
| 03 | RPM, DNF & Repositories | 8 — implementação v0.9.0 |

Total após esta entrega: **26 labs**.

## Próximos blocos

| Objective | Tema | Labs estimados |
|---|---|---:|
| 04 | Shell scripting para EX200 | 7 |
| 05 | Processos e serviços systemd | 9 |
| 06 | Networking / NetworkManager | 8 |
| 07 | Scheduling, logs e chrony | 8 |
| 08 | Storage, swap e LVM | 12 |
| 09 | Boot, GRUB e recuperação | 7 |
| 10 | SELinux e firewalld | 9 |
| 11 | NFS e autofs | 6 |
| 12 | Simulados integrados EX200 | 6 |

## Infraestrutura determinística de software

Objective 03 não depende de uma versão específica publicada na CDN.
`ansible/prepare-objective03.yml` cria repositórios locais com pequenos RPMs
originais de laboratório:

- base repository;
- errata repository;
- RPMs locais para inspeção/instalação.

Isso permite praticar RPM/DNF reais e manter a regressão reproduzível.
