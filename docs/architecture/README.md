# Arquitetura

```text
                        GitHub
                          ^
                          |
                       Git push
                          |
                    +-----+-----+
                    |  bastion  |
                    | Control   |
                    |  Plane    |
                    +-----+-----+
                       /     \
          Ansible/SSH /       \ Ansible/SSH
                     v         v
               +---------+ +---------+
               | servera | | serverb |
               | prática | |  apoio  |
               +---------+ +---------+
                    \         /
                     \       /
                  KVM / libvirt
                       |
                  Ubuntu Host
```

## Responsabilidades

### bastion
- Ansible Control Node
- futuro Python `lab` CLI
- graders e relatórios
- assets dos exercícios
- serviços auxiliares
- integração controlada com reset/snapshot

### servera
Máquina principal do candidato. Deve permanecer descartável e recuperável.

### serverb
Servidor auxiliar para NFS, SSH, rede, sincronização de tempo e testes remotos.

### Ubuntu Host
KVM, libvirt, virsh, snapshots, console e power control.
