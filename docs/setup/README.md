# Instalação do laboratório — comece por aqui

[Home](../../README.md)

Este conjunto de documentos descreve a implantação completa do ambiente local utilizado pelo projeto **RHCSA EX200 v10 Lab**.

O roteiro parte de um hospedeiro Linux com KVM/libvirt e termina com o primeiro laboratório executado pelo estudante.

A instalação foi organizada para que cada etapa tenha:

- objetivo claro;
- local correto de execução;
- comandos;
- validações;
- resultado esperado;
- critério para avançar;
- troubleshooting quando necessário.

O objetivo é permitir que outra pessoa monte o ambiente sem depender do histórico de desenvolvimento do projeto.

---

## Fluxo completo de instalação

```text
01 — Requisitos e arquitetura
        ↓
02 — Preparação do host KVM/libvirt
        ↓
03 — Criação das máquinas virtuais
        ├── Método A — instalação manual pela ISO
        └── Método B — implantação pela imagem-base
        ↓
04 — Configuração inicial das VMs
        ↓
05 — Preparação do bastion e clonagem do projeto
        ↓
06 — Configuração e validação do Ansible
        ↓
07 — Baseline e snapshots
        ↓
08 — Primeiro exercício
```

---

## 1. Requisitos e arquitetura

[01 — Requisitos e arquitetura](01-requisitos.md)

Use esta etapa para confirmar:

- suporte à virtualização por hardware;
- recursos de CPU, memória e armazenamento;
- sistema operacional do hospedeiro;
- arquitetura das três VMs;
- plano de endereçamento;
- versão local do RHEL;
- diferenças entre o ambiente local e o alvo RHEL 10;
- escolha entre Método A e Método B.

Não avance sem confirmar que a faixa de rede utilizada pelo laboratório não conflita com sua LAN, VPN ou outra rede virtual.

---

## 2. Preparação do host KVM/libvirt

[02 — Preparação do host KVM/libvirt](02-host-kvm.md)

Nesta etapa são preparados:

- KVM/QEMU;
- libvirt;
- `virsh`;
- `virt-install`;
- `qemu-img`;
- Cockpit e/ou ferramentas gráficas;
- pool `default`;
- rede NAT `rhcsa-lab`;
- bridge `virbr-rhcsa`;
- gateway `192.168.100.1`.

A preparação suporta hospedeiros Ubuntu e sistemas da família RHEL/Rocky Linux.

---

## 3. Criação das máquinas virtuais

[03 — Criação das máquinas virtuais](03-criacao-vms.md)

O projeto oferece dois caminhos.

### 3.1 Método A — instalação manual

[3.1 — Instalação manual a partir da ISO](03a-instalacao-manual.md)

Escolha este método quando quiser praticar também:

- criação das VMs;
- instalação do RHEL;
- seleção correta dos discos;
- preparação do sistema desde o início.

Cada VM é criada individualmente e instalada a partir de uma mídia ISO oficial do RHEL.

### 3.2 Método B — imagem-base

[3.2 — Implantação a partir da imagem-base](03b-imagem-template.md)

Escolha este método quando quiser reduzir o tempo de reconstrução do ambiente.

O procedimento documenta:

- validação da imagem com SHA-256;
- verificação do QCOW2;
- preservação de uma cópia-mestre;
- criação de discos independentes;
- criação de `bastion`, `servera` e `serverb`;
- discos adicionais;
- validação de `machine-id`;
- validação de SSH host keys;
- verificação de RHSM;
- preparação e sanitização da imagem-base.

Os dois métodos convergem para a mesma etapa 04.

---

## 4. Configuração inicial das VMs

[04 — Configuração inicial das VMs](04-configuracao-vms.md)

Nesta etapa são configurados:

```text
bastion.lab.test   192.168.100.10
servera.lab.test   192.168.100.11
serverb.lab.test   192.168.100.12
```

Também são validados:

- hostname;
- endereço IP;
- gateway;
- resolução de nomes;
- usuário `student`;
- SSH;
- SELinux;
- firewalld;
- origem de pacotes;
- identidade individual das VMs;
- topologia de discos.

---

## 5. Preparação do bastion e clonagem

[05 — Preparação do bastion e clonagem](05-bastion-git.md)

O `bastion` funciona como plano de controle do laboratório.

Nesta etapa são preparados:

- Git;
- Ansible Core;
- Python;
- PyYAML;
- SSH;
- clone do projeto;
- chave SSH dedicada ao laboratório;
- acesso não interativo a `servera` e `serverb`;
- comando `lab`.

O projeto é esperado em:

```text
/home/student/rhcsa-ex200-v10-lab
```

---

## 6. Configuração e validação do Ansible

[06 — Configuração e validação do Ansible](06-validacao-ansible.md)

Esta etapa comprova que o plano de controle está funcional.

São validados:

- `ansible.cfg`;
- inventário;
- grupos `control` e `managed`;
- host key checking;
- SSH;
- `sudo` não interativo para automação;
- `ansible.builtin.ping`;
- `become`;
- baseline RHEL 9;
- dependências dos exercícios;
- `lab status`;
- catálogo dos laboratórios.

Não crie snapshots antes de concluir esta validação.

---

## 7. Baseline e snapshots

[07 — Baseline e snapshots](07-baseline.md)

O baseline cria um ponto de recuperação antes dos exercícios.

A política do projeto é:

```text
bastion
└── plano de controle estável

servera / serverb
└── nós descartáveis protegidos por snapshot
```

A documentação diferencia:

```text
lab finish
```

de:

```text
snapshot
```

`lab finish` é o mecanismo normal de limpeza de cada cenário.

Snapshots são utilizados como recuperação quando a limpeza normal não for suficiente.

---

## 8. Primeiro exercício

[08 — Primeiro exercício](08-primeiro-lab.md)

Esta etapa apresenta o fluxo normal de uso:

```text
lab status
lab list
lab show
lab start
lab grade
lab finish
```

O primeiro exercício do roteiro é:

```text
obj01-01 — Operações com arquivos
```

O tutorial explica o ciclo completo sem revelar a solução do exercício.

---

## Arquitetura final

Ao término da instalação:

```text
                         Host KVM/libvirt
                                |
                         rede rhcsa-lab
                         192.168.100.0/24
                                |
              +-----------------+-----------------+
              |                 |                 |
           bastion            servera           serverb
       192.168.100.10     192.168.100.11    192.168.100.12
              |                 |                 |
       Git / Ansible / lab   exercícios       exercícios
```

Funções:

| VM | Função |
|---|---|
| `bastion` | Plano de controle, Git, Ansible e CLI `lab` |
| `servera` | Principal alvo dos exercícios |
| `serverb` | Host auxiliar e serviços remotos |

---

## Convenções utilizadas no roteiro

### Onde executar

Cada guia informa onde o comando deve ser executado.

Os principais contextos são:

```text
Host KVM
bastion
servera
serverb
```

Não assuma que um comando de `virsh`, `qemu-img` ou manipulação de QCOW2 deve ser executado dentro de uma VM.

Da mesma forma, comandos `lab` devem ser executados no `bastion`.

### Comandos administrativos

Quando necessário, a documentação utiliza:

```bash
sudo
```

Não execute o projeto inteiro como `root`.

### Segurança

O roteiro mantém:

```text
SELinux habilitado
firewalld habilitado
SSH host key checking habilitado
```

A documentação não depende da desativação desses controles para funcionar.

### Credenciais

Não publique no repositório:

```text
senhas
chaves SSH privadas
tokens
activation keys
credenciais Red Hat
credenciais de nuvem
```

---

## Ambiente local e alvo de certificação

A versão atual do laboratório utiliza:

```text
RHEL 9.8
```

como base local.

O projeto toma:

```text
RHEL 10
```

como referência para o objetivo de certificação e para a classificação de compatibilidade dos exercícios.

A documentação e o CLI deixam essa distinção explícita.

---

## Método A ou Método B?

Use esta referência rápida:

| Situação | Método recomendado |
|---|---|
| Primeira montagem e interesse em praticar instalação do RHEL | Método A |
| Deseja reproduzir o ambiente desde a ISO | Método A |
| Já domina instalação de RHEL | Método B |
| Precisa reconstruir o laboratório rapidamente | Método B |
| Está preparando outro host KVM para estudos | Método B |
| Precisa evitar dependência de uma imagem-base | Método A |

Ambos devem produzir a mesma arquitetura final.

---

## Antes de começar

Confirme:

```text
[ ] host Linux disponível
[ ] virtualização por hardware habilitada
[ ] recursos suficientes para três VMs
[ ] espaço em disco suficiente para snapshots
[ ] rede 192.168.100.0/24 disponível
[ ] acesso administrativo ao hospedeiro
[ ] Método A ou Método B escolhido
```

Depois inicie por:

[01 — Requisitos e arquitetura](01-requisitos.md)

---

[Home](../../README.md)
