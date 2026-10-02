# Pré-requisitos e dependências do laboratório RHCSA / EX200

Este documento define a **baseline obrigatória das três VMs** antes de iniciar
os exercícios.

A ideia é simples: problemas de infraestrutura, ferramentas ausentes e
dependências de RPM devem ser resolvidos **antes** do aluno entrar no primeiro
lab. Os exercícios devem avaliar a habilidade RHCSA, e não falhar porque uma
ferramenta necessária ao ambiente não estava instalada.

## 1. Topologia mínima

| VM | Papel | IP |
|---|---|---|
| `bastion` | control plane / equivalente à workstation | `192.168.100.10` |
| `servera` | alvo principal dos exercícios | `192.168.100.11` |
| `serverb` | alvo auxiliar / serviços remotos | `192.168.100.12` |

Requisitos comuns:

- RHEL 9.8 nas VMs locais;
- nomes `bastion.lab.test`, `servera.lab.test` e `serverb.lab.test`;
- usuário `student`;
- SSH ativo;
- SELinux `Enforcing`;
- `firewalld` ativo;
- comunicação IP e resolução de nomes entre as VMs.

## 2. Dependências do bastion

O `bastion` precisa manter o control plane do projeto. Antes dos labs, deve
possuir pelo menos:

- `ansible-core`;
- `python3`;
- `git`;
- `openssh-clients`;
- `rsync`;
- `curl`;
- `dnf-plugins-core`;
- `tar`, `gzip`, `bzip2` e `xz`;
- `vim-enhanced`;
- `man-db` e `man-pages`.

Os repositórios locais RHEL BaseOS e AppStream precisam estar funcionais no
bastion. Eles são a fonte offline de RPMs para `servera` e `serverb`.

## 3. Dependências de servera e serverb

As duas VMs de prática recebem uma baseline idêntica. Ela contém ferramentas
usadas por vários domínios do RHCSA:

### Essential Tools

- `tar`;
- `gzip`;
- `bzip2`;
- `xz`;
- `vim-enhanced`;
- `man-db`;
- `man-pages`;
- `openssh-clients`;
- `rsync`;
- `tree`.

### Arquivos, permissões e diagnóstico

- `acl`;
- `attr`;
- `lsof`;
- `psmisc`.

### SELinux

- `policycoreutils-python-utils`;
- `setools-console`.

### Storage

- `parted`;
- `lvm2`;
- `xfsprogs`;
- `e2fsprogs`.

### NFS e automount

- `nfs-utils`;
- `autofs`.

### Rede, serviços e segurança

- `NetworkManager`;
- `firewalld`;
- `chrony`;
- `httpd`.

> A instalação da baseline **não significa que todos os serviços ficam
> habilitados ou iniciados**. Os labs continuam responsáveis por configurar
> estado, persistência, firewall, SELinux e demais requisitos.

## 4. O que não deve ser escondido pela baseline

A baseline é infraestrutura, não solução de prova.

Quando o objetivo de um exercício for explicitamente **instalar ou remover
software**, o lab deve usar um pacote definido para aquela tarefa e não
considerar a instalação prévia como resposta.

Assim preservamos as duas coisas:

1. ambiente estável para os labs;
2. prática real de gerenciamento de pacotes.

## 5. Instalação da baseline

Após criar as VMs, configurar rede, SSH e os repositórios locais do bastion,
execute uma única vez:

```bash
cd ~/rhcsa-ex200-v10-lab
bash bootstrap/20-install-dependencies.sh
```

O bootstrap:

1. instala as dependências do control plane;
2. usa os repositórios locais do bastion;
3. baixa um conjunto completo de RPMs e dependências;
4. copia o bundle para `servera` e `serverb`;
5. instala os pacotes sem depender de RHSM ou Internet;
6. remove o bundle temporário dos alvos;
7. valida os comandos obrigatórios.

Resultado esperado:

```text
DEPENDENCY BASELINE: READY
```

## 6. Validação isolada

A qualquer momento:

```bash
cd ~/rhcsa-ex200-v10-lab
ANSIBLE_CONFIG=ansible/ansible.cfg ansible-playbook ansible/playbooks/00-validate-dependencies.yml
```

Nenhum lab deve ser iniciado enquanto essa validação apresentar um comando
`MISSING`.

## 7. Ordem de preparação do ambiente

Use esta ordem para uma instalação nova:

```text
Criar as três VMs
        ↓
Configurar rede / nomes / SSH
        ↓
Configurar BaseOS + AppStream no bastion
        ↓
Validar Ansible inventory
        ↓
Executar bootstrap/20-install-dependencies.sh
        ↓
Criar snapshot baseline
        ↓
Executar tests/release-gate.sh
        ↓
Iniciar os labs
```

O snapshot das VMs deve ser criado **depois** da instalação desta baseline.
Assim um reset retorna para um ambiente já pronto para todos os exercícios.
