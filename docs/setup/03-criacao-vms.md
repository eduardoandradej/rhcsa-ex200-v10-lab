# 03 — Criação das máquinas virtuais

[Índice](README.md) · [Home](../../README.md) · [Anterior](02-host-kvm.md) · [Próximo](04-configuracao-vms.md)

Nesta etapa são criadas as três máquinas virtuais que formam o ambiente do laboratório:

| Máquina | Função principal | RAM | vCPU | Disco do sistema |
|---|---|---:|---:|---:|
| `bastion` | Estação de controle, Git, Ansible e comando `lab` | 2 GiB | 2 | 30 GiB |
| `servera` | Alvo principal dos exercícios | 3 GiB | 2 | 30 GiB |
| `serverb` | Alvo auxiliar dos exercícios | 2 GiB | 2 | 30 GiB |

O projeto oferece dois métodos de implantação. Escolha apenas um deles.

## 3.1 Método A — instalação manual a partir da ISO do RHEL

Neste método, cada máquina virtual é criada individualmente e o Red Hat Enterprise Linux é instalado a partir da mídia oficial.

É o caminho recomendado para quem deseja praticar também:

- criação das VMs;
- instalação do RHEL;
- seleção do disco de instalação;
- configuração inicial do sistema;
- preparação completa do ambiente desde o início.

[Seguir o Método A — instalação manual](03a-instalacao-manual.md)

## 3.2 Método B — implantação a partir de uma imagem-base

Neste método, uma imagem QCOW2 previamente preparada é utilizada como ponto de partida para as três máquinas virtuais.

O objetivo é reduzir o tempo necessário para montar o ambiente e permitir que o estudante chegue mais rapidamente aos laboratórios RHCSA.

Mesmo utilizando a imagem-base, cada VM será individualizada antes do uso, recebendo:

- disco próprio;
- identidade própria;
- hostname próprio;
- endereço IP próprio;
- endereço MAC próprio;
- novas chaves SSH do host;
- registro Red Hat individual, quando aplicável.

[Seguir o Método B — imagem-base/template](03b-imagem-template.md)

## Qual método escolher?

| Situação | Método recomendado |
|---|---|
| Primeira montagem do laboratório | Método A |
| Deseja aprender também a instalação do RHEL | Método A |
| Deseja reproduzir todo o processo manualmente | Método A |
| Já conhece instalação de RHEL | Método B |
| Precisa reconstruir rapidamente o laboratório | Método B |
| Novo host KVM para demonstrações ou estudos | Método B |

Os dois métodos devem resultar na mesma arquitetura lógica:

```text
                    Host KVM/libvirt
                          |
                    rhcsa-lab
                  192.168.100.0/24
                          |
          +---------------+---------------+
          |               |               |
       bastion          servera         serverb
   192.168.100.10   192.168.100.11  192.168.100.12