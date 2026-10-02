# 01 — Requisitos e arquitetura

[Índice](README.md) · [Home](../../README.md) · [Próximo](02-host-kvm.md)

Este roteiro começa com um host Linux e termina com o primeiro exercício executado pelo estudante. O provisionamento das VMs é manual; o Ansible entra depois, no bastion, para preparar e avaliar cenários.

## Plataforma e requisitos

A base atual do projeto usa **RHEL 9.8 nas três VMs** e toma **RHEL 10 como referência de estudo**. O playbook `validate.yml` atual exige Red Hat Enterprise Linux 9. Usar RHEL 10 requer revisar essa validação e a compatibilidade dos exercícios; não basta trocar a ISO.

Os comandos do host deste roteiro são para **Rocky Linux 9 / RHEL 9**, com KVM/libvirt. Outros sistemas precisam de adaptação dos pacotes e serviços.

Dimensionamento inicial sugerido, não um mínimo certificado:

| Máquina | vCPU | RAM | Disco do sistema | Discos extras |
|---|---:|---:|---:|---|
| bastion | 2 | 2 GiB | 30 GiB | nenhum |
| servera | 2 | 3 GiB | 30 GiB | 5 + 5 + 3 + 2 GiB |
| serverb | 2 | 2 GiB | 30 GiB | 5 + 3 GiB |

Reserve memória para o host; 16 GiB de RAM é uma configuração inicial confortável. Reserve pelo menos 120 GiB livres para sistemas, ISO e crescimento dos snapshots. A necessidade real varia com exercícios e retenção. SSD é preferível.

Pré-requisitos: CPU x86_64 com AMD-V/VT-x habilitado no firmware; host Linux instalado; acesso administrativo; ISO DVD do RHEL obtida legalmente e compatível com a versão das VMs; espaço em disco; conexão para obter o projeto e dependências. A ISO e materiais oficiais não são distribuídos aqui.

## Rede isolada de prática

| Elemento | Endereço | Papel |
|---|---|---|
| Rede libvirt `rhcsa-lab` | 192.168.100.0/24 | NAT do laboratório |
| Interface do host `virbr-rhcsa` | 192.168.100.1 | gateway/DNS das VMs |
| bastion | 192.168.100.10 | estação do aluno e automação |
| servera | 192.168.100.11 | alvo principal |
| serverb | 192.168.100.12 | alvo auxiliar |

Domínio usado no roteiro: `lab.example`. Verifique se 192.168.100.0/24 conflita com LAN, VPN ou outra rede libvirt. Se conflitar, escolha outra faixa e atualize rede, VMs, resolução de nomes e inventário juntos.

O host KVM executa `virsh` e cria as VMs. O bastion executa Git, Ansible e `lab`. As tarefas dos exercícios são resolvidas manualmente em servera/serverb. Não é necessário clonar o projeto no host para seguir as etapas 2 a 4.

**Antes de avançar:** confirme a ISO, os recursos disponíveis e uma faixa de rede sem conflito.

[Índice](README.md) · [Home](../../README.md) · [Próximo](02-host-kvm.md)
