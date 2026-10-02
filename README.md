# RHCSA EX200 v10 Lab

Laboratório comunitário e **não oficial** para prática hands-on de administração Red Hat Enterprise Linux, orientado aos objetivos atuais do RHCSA / EX200.

## Comece por aqui

Monte o ambiente antes de executar a automação. Siga os guias na ordem:

1. [Requisitos e arquitetura](docs/setup/01-requisitos.md)
2. [Preparação do host KVM/libvirt](docs/setup/02-host-kvm.md)
3. [Criação das máquinas virtuais](docs/setup/03-criacao-vms.md)
4. [Configuração inicial das VMs](docs/setup/04-configuracao-vms.md)
5. [Preparação do bastion e clonagem](docs/setup/05-bastion-git.md)
6. [Configuração e validação do Ansible](docs/setup/06-validacao-ansible.md)
7. [Baseline e snapshots](docs/setup/07-baseline.md)
8. [Primeiro exercício](docs/setup/08-primeiro-lab.md)

**Já tem as VMs prontas?** Confira a [configuração inicial](docs/setup/04-configuracao-vms.md) e siga para o [bastion e Git](docs/setup/05-bastion-git.md).

O roteiro de instalação e o roadmap de desenvolvimento têm funções diferentes: os guias explicam como montar o ambiente; o roadmap mostra as funcionalidades implementadas e pendentes.

## Hospedeiro e imagens

O laboratório foi montado em um hospedeiro **Ubuntu Desktop com KVM/libvirt**. O guia usa Ubuntu como caminho principal e documenta **Rocky Linux 9.8 como alternativa de host**. O hospedeiro deve ter interface Desktop; a alternativa Rocky também deve incluir ambiente gráfico. A preparação inclui **Cockpit + cockpit-machines** para consultas rápidas pelo navegador. As VMs da base atual são RHEL 9.8.

Veja [downloads oficiais e configuração do ambiente](docs/setup/01-requisitos.md#imagens-e-downloads-oficiais) e [preparação do host Ubuntu ou Rocky](docs/setup/02-host-kvm.md). O hospedeiro de referência é um **ThinkPad T430**, com **Ubuntu Desktop 24.04.5 LTS**, **Intel Core i5-3320M (2 núcleos / 4 threads)**, **15 GiB de RAM reportados**, **4 GiB de swap** e **SSD Kingston de 240 GB**. Veja a [configuração real do hospedeiro](docs/setup/01-requisitos.md#configuração-real-do-hospedeiro). O dimensionamento das VMs no guia é uma sugestão de instalação, não uma medição das VMs existentes.

## Visão geral

Este projeto usa:

- **RHEL 9.8** como plataforma local de execução;
- **RHEL 10** como referência de conteúdo e objetivos de estudo;
- **KVM/libvirt** para virtualização;
- **bastion** como Control Plane;
- **servera** como alvo principal de prática;
- **serverb** como servidor auxiliar;
- **Ansible** para preparar, limpar e validar cenários;
- **Python** para o CLI `lab` e graders;
- **Git/GitHub** para versionamento e documentação.

> A automação prepara e avalia o ambiente. O estudante resolve manualmente as tarefas de administração.

## Arquitetura

| Host | IP | Papel |
|---|---|---|
| bastion | 192.168.100.10 | Control Plane / automação |
| servera | 192.168.100.11 | alvo principal de prática |
| serverb | 192.168.100.12 | apoio / serviços remotos |

### Storage de prática

`servera`

- `vdb` 5 GiB
- `vdc` 5 GiB
- `vdd` 3 GiB
- `vde` 2 GiB

`serverb`

- `vdb` 5 GiB
- `vdc` 3 GiB

## Primeiro teste do Control Plane

Execute somente depois de concluir a [preparação do bastion](docs/setup/05-bastion-git.md).
O teste completo está no [guia de validação do Ansible](docs/setup/06-validacao-ansible.md).

## Roadmap

- [x] KVM/libvirt com bastion, servera e serverb
- [x] discos adicionais de prática
- [x] snapshots de baseline
- [x] repositórios locais RHEL 9.8
- [x] Git + Ansible no bastion
- [x] SSH sem senha bastion -> servera/serverb
- [x] inventory Ansible funcional
- [x] `lab list`
- [x] `lab start`
- [x] `lab grade`
- [x] `lab finish`
- [ ] reset seguro via host-control
- [ ] serviços auxiliares no bastion
- [x] primeiros labs do Objetivo 01 (consulte `lab list` para saber quais estão `ready`)
- [ ] expansão dos labs por objetivo
- [ ] mock exams

## Compatibilidade

A infraestrutura local usa RHEL 9.8 por limitação de hardware. Os exercícios serão classificados por compatibilidade:

- **RHEL 9.8 = RHEL 10**: execução equivalente;
- **RHEL 9.8 ≈ RHEL 10**: pequenas diferenças de implementação;
- **RHEL 10 only**: validar em ambiente RHEL 10.

## Aviso

Este é um projeto comunitário e não oficial.

Red Hat, Red Hat Enterprise Linux, RHCSA e EX200 são marcas da Red Hat, Inc. Este repositório não é afiliado, patrocinado ou endossado pela Red Hat.

Materiais oficiais de treinamento não são redistribuídos neste projeto. Os exercícios públicos serão autorais e baseados em objetivos públicos do exame e em tarefas gerais de administração Linux.

## Licença

Apache License 2.0.
