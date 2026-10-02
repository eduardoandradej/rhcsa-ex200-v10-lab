# RHCSA EX200 v10 Lab

Laboratório comunitário e **não oficial** para prática hands-on de administração Red Hat Enterprise Linux, orientado aos objetivos atuais do RHCSA / EX200.

## Visão geral

Este projeto usa:

- **RHEL 9.8** como plataforma local de execução;
- **RHEL 10** como referência de conteúdo e objetivos de estudo;
- **KVM/libvirt** para virtualização;
- **bastion** como Control Plane;
- **servera** como alvo principal de prática;
- **serverb** como servidor auxiliar;
- **Ansible** para preparar, limpar e validar cenários;
- **Python** para o futuro CLI `lab` e graders;
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

No `bastion`:

```bash
cd ~/rhcsa-ex200-v10-lab/ansible
ansible-inventory --graph
ansible managed -m ansible.builtin.ping
ansible managed -m ansible.builtin.command -a "hostname -f"
```

## Roadmap

- [x] KVM/libvirt com bastion, servera e serverb
- [x] discos adicionais de prática
- [x] snapshots de baseline
- [x] repositórios locais RHEL 9.8
- [x] Git + Ansible no bastion
- [x] SSH sem senha bastion -> servera/serverb
- [x] inventory Ansible funcional
- [ ] `lab list`
- [ ] `lab start`
- [ ] `lab grade`
- [ ] `lab finish`
- [ ] reset seguro via host-control
- [ ] serviços auxiliares no bastion
- [ ] labs por objetivo
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
