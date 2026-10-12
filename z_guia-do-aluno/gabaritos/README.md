# RHCSA EX200 v10 — Gabaritos Operacionais

**Caderno de consulta: 100 exercícios distribuídos em 12 objetivos.**  
Ambiente de referência: RHEL 9.8 | Alvo de estudos: RHCSA/EX200 em RHEL 10.

> **Atenção: estes arquivos contêm soluções.** Utilize-os preferencialmente após tentar resolver os exercícios, consultar o resultado de `lab grade` e investigar os critérios pendentes. São exercícios autorais do projeto independente, não questões do exame oficial da Red Hat.

## Índice por objetivo

| Objective | Tema | Labs | Gabarito |
|:---:|---|---:|---|
| 01 | Essential Tools | 10 | [Abrir OBJ01](OBJ01_Essential_Tools_Comandos.md) |
| 02 | Users & Groups | 8 | [Abrir OBJ02](OBJ02_Users_Groups_Comandos.md) |
| 03 | RPM, DNF & Repositories | 8 | [Abrir OBJ03](OBJ03_RPM_DNF_Repositories_Comandos.md) |
| 04 | Simple Shell Scripts | 8 | [Abrir OBJ04](OBJ04_Shell_Scripts_Comandos.md) |
| 05 | Processes, Scheduling, Tuning & systemd | 10 | [Abrir OBJ05](OBJ05_Processes_Systemd_Comandos.md) |
| 06 | NetworkManager, IP Networking & Name Resolution | 8 | [Abrir OBJ06](OBJ06_NetworkManager_Comandos.md) |
| 07 | Scheduling, Temporary Files, Logging & Time | 8 | [Abrir OBJ07](OBJ07_Scheduling_Logging_Comandos.md) |
| 08 | Partitions, Filesystems, Swap & LVM | 12 | [Abrir OBJ08](OBJ08_Storage_LVM_Comandos.md) |
| 09 | Boot, GRUB & Recovery | 7 | [Abrir OBJ09](OBJ09_Boot_Recovery_Comandos.md) |
| 10 | SELinux & firewalld | 9 | [Abrir OBJ10](OBJ10_SELinux_Firewalld_Comandos.md) |
| 11 | NFS & AutoFS | 6 | [Abrir OBJ11](OBJ11_NFS_AutoFS_Comandos.md) |
| 12 | Comprehensive EX200 Challenges | 6 | [Abrir OBJ12](OBJ12_Integrated_Challenges_Comandos.md) |
| **Total** | | **100** | **12 documentos** |

## Como usar

1. No `bastion`, execute `lab start objXX-YY`.
2. Resolva no host indicado, seguindo o bloco de comandos correspondente.
3. Volte ao `bastion`, execute `lab grade objXX-YY` e, somente depois, `lab finish objXX-YY`.

> **Importante:** `obj09-04` e `obj09-06` são exercícios `manual-only` e seguem o procedimento próprio de console KVM/GRUB, sem os comandos usuais de `start`, `grade` ou `finish`.
>
> **Armazenamento:** nos exercícios destrutivos use apenas os discos scratch previstos, nunca `/dev/vda`. Confira o host e o disco antes de executar os comandos.

## Documentação do projeto

- [Guia operacional do aluno](../RHCSA-EX200-v10-Manual%20de%20execucao%20Laboratorios_.md)
- [README principal](../../README.md)
- [Repositório RHCSA EX200 v10 Lab](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab)

**Origem:** comandos organizados a partir dos enunciados e soluções de referência de QA do repositório, na versão consultada. A verificação sintática não substitui o teste funcional com `lab grade` nas VMs.
