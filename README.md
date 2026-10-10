<div align="center">

# RHCSA EX200 v10 Lab

**Laboratório hands-on independente para prática estruturada de administração Red Hat Enterprise Linux, com foco no RHCSA / EX200.**

![Release](https://img.shields.io/badge/release-v1.8.4-2f3136)
![Curriculum](https://img.shields.io/badge/curr%C3%ADculo-100%20itens-2f3136)
![Automated Labs](https://img.shields.io/badge/labs%20automatizados-98-2f3136)
![Manual Drills](https://img.shields.io/badge/drills%20manuais-2-2f3136)
![Local Platform](https://img.shields.io/badge/plataforma%20local-RHEL%209.8-2f3136)
![Target](https://img.shields.io/badge/alvo-RHEL%2010%20%2F%20EX200-2f3136)
![License](https://img.shields.io/badge/licen%C3%A7a-Apache%202.0-2f3136)

</div>

---

## Visão geral

O **RHCSA EX200 v10 Lab** é um projeto independente para prática local, repetível e orientada a estado final de competências de administração Linux/RHEL.

O ambiente foi construído para reproduzir uma rotina de estudo hands-on em três máquinas virtuais:

- `bastion`: plano de controle;
- `servera`: principal alvo de prática;
- `serverb`: host auxiliar e provedor de serviços remotos.

A automação **prepara o cenário, valida o ambiente e avalia o estado final**. O estudante continua responsável por resolver as tarefas manualmente.

```text
Automação prepara
       ↓
Estudante resolve
       ↓
Grader avalia o estado final
       ↓
Cleanup restaura o cenário
```

O projeto não depende de respostas exatas ou de uma sequência única de comandos. O que importa é atingir o estado solicitado pelo exercício.

> O termo **v10** no nome do projeto se refere ao alvo de estudo baseado em RHEL 10 / EX200. A plataforma local atualmente validada pelo projeto é RHEL 9.8.

---

## Estado atual do projeto

| Item | Estado |
|---|---|
| Currículo | Concluído |
| Objetivos | 12 |
| Itens de aprendizagem | 100 |
| Labs automatizados e avaliáveis em runtime | 98 |
| Exercícios manuais de recuperação por console | 2 |
| CLI `lab` | Implementado |
| Setup / grade / cleanup | Implementados |
| Release gate | Implementado |
| Regression runner de referência | Implementado |
| Plataforma local | RHEL 9.8 |
| Alvo de estudo | RHEL 10 / RHCSA EX200 |
| Virtualização | KVM/libvirt |
| Licença | Apache License 2.0 |
| Base estável atual | `v1.8.4` |

O detalhamento do currículo está em [docs/ROADMAP.md](docs/ROADMAP.md).

---

# Arquitetura

```text
                              GitHub
                                 |
                                 | clone / pull
                                 v
                    +--------------------------+
                    |         bastion          |
                    |     Control Plane        |
                    |  Git / Ansible / lab     |
                    |     192.168.100.10       |
                    +------------+-------------+
                                 |
                         SSH / Ansible
                     +-----------+-----------+
                     |                       |
                     v                       v
          +--------------------+   +--------------------+
          |      servera       |   |      serverb       |
          |  alvo principal    |   |   host auxiliar    |
          |  192.168.100.11    |   |  192.168.100.12    |
          +--------------------+   +--------------------+
                     \                       /
                      \                     /
                       +-------------------+
                       |   rhcsa-lab NAT   |
                       | 192.168.100.0/24  |
                       +---------+---------+
                                 |
                       +---------v---------+
                       |  Host KVM/libvirt |
                       | snapshots/console |
                       +-------------------+
```

## Papéis

| Componente | Responsabilidade |
|---|---|
| `bastion` | Git, Ansible, CLI `lab`, graders, estado dos exercícios e automação |
| `servera` | Principal máquina de prática do estudante |
| `serverb` | NFS, AutoFS, SSH, rede, serviços auxiliares e cenários distribuídos |
| Host KVM | Criação das VMs, discos, console, snapshots e recuperação out-of-band |

O `bastion` é mantido estável. `servera` e `serverb` são tratados como nós descartáveis e recuperáveis.

---

# Topologia de armazenamento

## `servera`

| Disco | Tamanho | Uso |
|---|---:|---|
| `vda` | 30 GiB | Sistema operacional — protegido |
| `vdb` | 5 GiB | Scratch / exercícios |
| `vdc` | 5 GiB | Scratch / exercícios |
| `vdd` | 3 GiB | Scratch / exercícios |
| `vde` | 2 GiB | Scratch / exercícios |

## `serverb`

| Disco | Tamanho | Uso |
|---|---:|---|
| `vda` | 30 GiB | Sistema operacional — protegido |
| `vdb` | 5 GiB | Scratch / exercícios |
| `vdc` | 3 GiB | Scratch / exercícios |

Os exercícios destrutivos de armazenamento são limitados aos discos de scratch autorizados. O contrato de segurança do Objective 08 está documentado em [docs/OBJ08-STORAGE-SAFETY.md](docs/OBJ08-STORAGE-SAFETY.md).

---

# Currículo

O catálogo atual possui **100 itens de aprendizagem**, distribuídos em 12 objetivos.

| Objective | Tema | Itens |
|---|---|---:|
| 01 | Essential Tools | 10 |
| 02 | Users & Groups | 8 |
| 03 | RPM, DNF & Repositories | 8 |
| 04 | Simple Shell Scripts | 8 |
| 05 | Processes, Scheduling, Tuning & systemd | 10 |
| 06 | Networking / NetworkManager | 8 |
| 07 | Scheduling, Temporary Files, Logging & Time | 8 |
| 08 | Partitions, Filesystems, Swap & LVM | 12 |
| 09 | Boot, GRUB & Recovery | 7 |
| 10 | SELinux & firewalld | 9 |
| 11 | NFS & AutoFS | 6 |
| 12 | Comprehensive EX200 Challenges | 6 |
| **Total** |  | **100** |

No Objective 09:

- 5 itens são automatizados;
- 2 são exercícios manuais de recuperação via console.

Isso resulta em:

```text
98 labs automatizados
 2 drills manuais
-------------------
100 itens de aprendizagem
```

Consulte o [roadmap completo](docs/ROADMAP.md).

---

# Filosofia do laboratório

O projeto segue quatro princípios.

## 1. O estudante resolve manualmente

Ansible não resolve a tarefa do estudante.

Ele é utilizado para:

- preparar infraestrutura;
- criar cenários;
- restaurar estado;
- instalar dependências;
- executar validações auxiliares.

A solução continua sendo feita manualmente no sistema alvo.

## 2. O grader avalia estado final

Os graders não exigem uma resposta textual ou uma sequência específica de comandos.

Eles verificam o estado real do sistema.

Exemplos:

```text
arquivo existe?
permissão está correta?
serviço está habilitado?
porta SELinux está rotulada?
filesystem está montado?
LVM possui o tamanho esperado?
configuração persiste?
```

## 3. O cleanup é parte do contrato

Cada lab automatizado `ready` possui um ciclo:

```text
setup.yml
    ↓
student work
    ↓
grade.py
    ↓
finish.yml
```

O objetivo é permitir repetição consistente.

## 4. Segurança do host e do disco do sistema

O projeto não autoriza exercícios destrutivos contra `/dev/vda`.

Nos laboratórios de storage, os alvos destrutivos são limitados por allowlist e validados antes da execução.

---

# Instalação

A instalação completa está organizada em uma trilha sequencial:

1. [Requisitos e arquitetura](docs/setup/01-requisitos.md)
2. [Preparação do host KVM/libvirt](docs/setup/02-host-kvm.md)
3. [Criação das máquinas virtuais](docs/setup/03-criacao-vms.md)
4. [Configuração inicial das VMs](docs/setup/04-configuracao-vms.md)
5. [Preparação do bastion e clonagem](docs/setup/05-bastion-git.md)
6. [Configuração e validação do Ansible](docs/setup/06-validacao-ansible.md)
7. [Baseline e snapshots](docs/setup/07-baseline.md)
8. [Primeiro exercício](docs/setup/08-primeiro-lab.md)

O ponto de entrada recomendado é:

[**Instalação do laboratório — comece por aqui**](docs/setup/README.md)

---

# Dois métodos de criação das VMs

A etapa 03 oferece dois caminhos.

## Método A — instalação manual

[3.1 — Instalação manual a partir da ISO](docs/setup/03a-instalacao-manual.md)

Recomendado para quem deseja praticar também:

- criação das máquinas virtuais;
- instalação do RHEL;
- seleção correta do disco de sistema;
- preparação completa do ambiente desde a mídia oficial.

## Método B — imagem-base QCOW2

[3.2 — Implantação a partir da imagem-base](docs/setup/03b-imagem-template.md)

Recomendado para:

- reconstrução rápida do laboratório;
- novos hosts KVM;
- ambientes de demonstração;
- recuperação completa do ambiente de estudos.

O método documenta:

- validação SHA-256;
- `qemu-img check`;
- preservação da imagem-mestre;
- criação de discos independentes;
- individualização das VMs;
- `machine-id`;
- SSH host keys;
- RHSM;
- preparação e sanitização da imagem.

> O repositório não armazena ISOs ou imagens QCOW2 do RHEL. Qualquer disponibilização pública de uma imagem RHEL deve observar os termos de redistribuição aplicáveis.

Os dois métodos convergem para a mesma arquitetura final.

---

# Hospedeiro

O caminho principal documentado utiliza:

```text
Ubuntu Desktop 24.04 LTS
KVM/QEMU
libvirt
virt-install
qemu-img
Cockpit
cockpit-machines
```

Também existe um caminho documentado para:

```text
RHEL 9
Rocky Linux 9
```

O projeto não exige que o hospedeiro seja uma instalação Server. Um desktop Linux com KVM/libvirt é perfeitamente adequado ao ambiente de estudo.

Consulte [02 — Preparação do host KVM/libvirt](docs/setup/02-host-kvm.md).

---

# CLI `lab`

O controlador local é executado no `bastion`.

```bash
lab --version
```

## Comandos

| Comando | Função |
|---|---|
| `lab status` | Verifica Control Plane, nós e ferramentas essenciais |
| `lab list` | Lista o catálogo de exercícios |
| `lab list --objective obj08` | Filtra por objetivo |
| `lab show obj01-01` | Exibe metadados e enunciado |
| `lab show obj01-01 --lang en` | Exibe o enunciado em inglês |
| `lab start obj01-01` | Prepara e ativa o cenário |
| `lab grade obj01-01` | Avalia o estado final |
| `lab grade` | Avalia o laboratório atualmente ativo |
| `lab finish obj01-01` | Executa cleanup e encerra o cenário |
| `lab finish` | Finaliza o laboratório atualmente ativo |

---

# Fluxo de estudo

```bash
lab status
lab list --objective obj01
lab show obj01-01
lab start obj01-01
```

Depois o estudante acessa o host alvo e resolve manualmente a tarefa.

Ao terminar:

```bash
lab grade obj01-01
```

Se necessário:

```text
FAIL
 ↓
investigar
 ↓
corrigir manualmente
 ↓
grade novamente
```

Quando concluir:

```bash
lab finish obj01-01
lab status
```

O ambiente deve retornar para:

```text
Active      none
Environment READY
```

---

# Compatibilidade RHEL 9.8 / RHEL 10

A plataforma local atualmente utilizada é:

```text
RHEL 9.8
```

O alvo de estudo é:

```text
RHEL 10 / RHCSA EX200
```

Cada exercício declara uma classificação de compatibilidade.

| Nível | Significado |
|---|---|
| `exact` | Execução equivalente no ambiente local e no alvo |
| `near` | Objetivo válido, mas existe diferença relevante entre versões |
| `rhel10-only` | Deve ser validado em ambiente RHEL 10 |

Exemplo de manifesto:

```yaml
compatibility:
  local: "RHEL 9.8"
  target: "RHEL 10"
  level: exact
```

Consulte [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md).

Para itens classificados como `near` ou `rhel10-only`, utilize também um ambiente RHEL 10 apropriado, como os labs disponíveis por uma assinatura Red Hat Learning Subscription.

---

# Boot e recuperação

O Objective 09 possui dois exercícios deliberadamente manuais:

```text
obj09-04 — rescue/emergency boot via GRUB
obj09-06 — recuperação de acesso root pelo boot loader
```

Eles não são tratados como uma deficiência do currículo.

O `bastion` não recebe controle privilegiado do hypervisor apenas para automatizar interação pré-boot com GRUB.

Esses exercícios devem ser realizados pelo console gráfico/libvirt e, quando necessário, repetidos em um ambiente RHEL 10.

Consulte [docs/OBJ09-BOOT-RECOVERY.md](docs/OBJ09-BOOT-RECOVERY.md).

---

# Baseline e recuperação

A política de recuperação separa cleanup normal de recuperação out-of-band.

```text
lab finish
└── limpeza normal do exercício

snapshot
└── recuperação da VM quando o cleanup normal não é suficiente
```

O baseline recomendado protege:

```text
servera
serverb
```

O `bastion` permanece estável e versionado pelo Git.

Consulte [07 — Baseline e snapshots](docs/setup/07-baseline.md).

---

# Engenharia e QA

O repositório possui uma camada própria de validação de engenharia.

## Release gate

`tests/release-gate.sh` verifica, entre outros pontos:

- sintaxe Python sem geração de `__pycache__`;
- sintaxe dos scripts shell;
- contrato YAML do catálogo;
- arquivos obrigatórios de labs `ready`;
- contrato `--json` dos graders;
- sintaxe dos playbooks Ansible;
- smoke test do CLI;
- gates específicos de objetivos;
- contratos de segurança de storage, networking, SELinux/firewalld, NFS/AutoFS e desafios integrados.

Execução:

```bash
bash tests/release-gate.sh
```

## Reference integration runner

O projeto inclui:

```text
tests/integration-reference.sh
```

e soluções de referência de QA para os **98 labs automatizados**.

O runner executa, para cada lab:

```text
lab start
    ↓
reference solution
    ↓
lab grade
    ↓
Score: 100%
    ↓
lab finish
```

As soluções de referência existem para validar o contrato entre cenário, grader e cleanup.

Elas não substituem a prática manual do estudante.

---

# Estrutura do repositório

```text
rhcsa-ex200-v10-lab/
├── ansible/
│   ├── inventory/
│   ├── playbooks/
│   └── vars/
│
├── bin/
│   └── lab
│
├── bootstrap/
│   └── instalação do CLI e preparação inicial
│
├── docs/
│   ├── setup/
│   ├── releases/
│   ├── development/
│   └── documentação por objetivo
│
├── labctl/
│   └── implementação Python do controlador
│
├── labs/
│   └── objetivos e exercícios
│
├── tests/
│   ├── reference-solutions/
│   ├── integration-reference.sh
│   └── release gates
│
├── LICENSE
├── README.md
└── SUPPORT.md
```

Um lab automatizado típico contém:

```text
lab.yml
prompt.pt.md
prompt.en.md
setup.yml
grade.py
finish.yml
solution.md
```

---

# Contrato de um lab `ready`

O release gate exige, para um lab marcado como `ready`, os arquivos:

```text
setup.yml
finish.yml
grade.py
prompt.pt.md
prompt.en.md
solution.md
```

O manifesto `lab.yml` contém metadados como:

```yaml
id: obj01-01
title: "Operações com arquivos"
objective: "Objective 01 — Essential Tools"

target:
  - servera

difficulty: 1
duration: 10

compatibility:
  local: "RHEL 9.8"
  target: "RHEL 10"
  level: exact

reset_policy: ansible
status: ready
```

Isso permite tratar o catálogo como dados estruturados, e não como uma coleção informal de scripts.

---

# Segurança e limites do projeto

O laboratório foi construído para continuar ensinando administração real de Linux sem depender de desativação de controles.

A preparação preserva:

```text
SELinux
firewalld
SSH host key checking
sudo controlado
libvirt no host
separação entre Control Plane e nós de prática
```

O repositório não deve conter:

```text
senhas
tokens
chaves SSH privadas
activation keys
credenciais Red Hat
credenciais de nuvem
ISOs do RHEL
imagens QCOW2 do RHEL
```

Não desabilite SELinux, firewalld ou verificação de host keys apenas para fazer um exercício passar.

---

# Conteúdo oficial e independência

Este é um **projeto independente, comunitário e não oficial**.

Ele não é:

- um produto da Red Hat;
- um simulador oficial do EX200;
- uma reprodução da Red Hat Learning Subscription;
- um repositório de questões reais de exame;
- um espelho de materiais proprietários da Red Hat.

Os exercícios públicos deste projeto são autorais e voltados à prática de competências de administração Linux/RHEL.

Red Hat, Red Hat Enterprise Linux, RHEL, RHCSA e demais marcas mencionadas pertencem aos seus respectivos titulares.

---

# Releases

A documentação das versões está em:

[docs/releases/](docs/releases/)

A base estável utilizada na revisão atual é:

```text
v1.8.4
```

Detalhes:

[v1.8.4 — OBJ12-06 protected report evidence hotfix](docs/releases/v1.8.4.md)

Para identificar a versão da sua cópia:

```bash
git describe --tags --always
```

---

# Roadmap

O currículo de 12 objetivos está concluído.

O foco de evolução passa a ser:

- correções de bugs;
- melhoria da documentação;
- experiência de instalação;
- compatibilidade com RHEL 10;
- segurança dos resets;
- QA e regressão;
- relatórios e experiência do usuário.

Consulte:

[docs/ROADMAP.md](docs/ROADMAP.md)

---

# Apoie o projeto

O projeto é desenvolvido e mantido de forma independente e disponibilizado gratuitamente.

Se ele estiver contribuindo para seus estudos e você quiser apoiar voluntariamente sua manutenção e evolução:

[**Apoie o projeto**](SUPPORT.md)

O apoio não condiciona acesso aos laboratórios, documentação ou funcionalidades.

---

# Licença

Código e documentação deste repositório são disponibilizados sob a:

**Apache License 2.0**

Consulte [LICENSE](LICENSE).

```text
Copyright 2026 Eduardo Andrade
```

---

# Autor e perfis profissionais

**Eduardo Andrade**

Projeto desenvolvido como ambiente independente de prática, experimentação e preparação hands-on em administração Red Hat Enterprise Linux.

- **LinkedIn:** [linkedin.com/in/eduardoandradej](https://www.linkedin.com/in/eduardoandradej)
- **Credly:** [credly.com/users/eduardoandradej](https://www.credly.com/users/eduardoandradej)

---

<div align="center">

**RHCSA EX200 v10 Lab**

Automação para preparar e avaliar.
Administração Linux para ser praticada de verdade.

</div>
