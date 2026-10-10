# 06 — Configuração e validação do Ansible

[Índice](README.md) · [Home](../../README.md) · [Anterior](05-bastion-git.md) · [Próximo](07-baseline.md)

**Onde executar:** `bastion`, conectado como usuário `student`, exceto quando o texto indicar explicitamente uma das VMs gerenciadas.

Esta etapa valida o plano de controle do laboratório antes da criação do baseline.

O objetivo não é apenas confirmar que o comando `ansible` está instalado. Antes de avançar, é necessário comprovar que:

- o inventário do projeto está sendo carregado;
- `bastion`, `servera` e `serverb` são identificados corretamente;
- o SSH por chave funciona para os hosts gerenciados;
- a verificação de host keys permanece habilitada;
- o Python está disponível nos destinos;
- a elevação de privilégios utilizada pela automação funciona sem interação;
- as três VMs correspondem ao baseline RHEL 9 utilizado pela versão atual do laboratório;
- as dependências necessárias aos exercícios estão disponíveis;
- o CLI `lab` consegue consultar o ambiente.

> Não crie snapshots de baseline de um ambiente que ainda apresente falhas nesta etapa.

---

## 6.1 Arquitetura do plano de controle

O Ansible é executado no `bastion`.

A arquitetura utilizada pelo projeto é:

```text
                         bastion
                    192.168.100.10
                            |
                    Ansible + lab CLI
                            |
              +-------------+-------------+
              |                           |
              | SSH                       | SSH
              |                           |
           servera                     serverb
      192.168.100.11              192.168.100.12
```

No inventário:

```text
control
└── bastion

managed
├── servera
└── serverb
```

O `bastion` utiliza conexão local do Ansible.

`servera` e `serverb` utilizam SSH com o usuário:

```text
student
```

e a chave:

```text
/home/student/.ssh/id_ed25519_rhcsa_lab
```

---

## 6.2 Confirmar o ponto de execução

Antes de continuar:

```bash
hostname -f
```

Resultado esperado:

```text
bastion.lab.test
```

Confira o usuário:

```bash
id -un
```

Resultado esperado:

```text
student
```

Entre na raiz do projeto:

```bash
cd ~/rhcsa-ex200-v10-lab
```

Confira:

```bash
pwd
```

Resultado esperado:

```text
/home/student/rhcsa-ex200-v10-lab
```

Valide o estado do repositório:

```bash
git status
```

Registre também a versão atual:

```bash
git describe --tags --always
```

---

## 6.3 Confirmar as ferramentas necessárias

Execute:

```bash
command -v ansible
command -v ansible-playbook
command -v ansible-inventory
command -v ssh
command -v git
command -v python3
```

Todos os comandos devem retornar um caminho.

Confira as versões:

```bash
ansible --version
```

```bash
python3 --version
```

Valide PyYAML:

```bash
python3 -c 'import yaml; print("PyYAML OK")'
```

Resultado esperado:

```text
PyYAML OK
```

Se alguma dependência estiver ausente, retorne à etapa:

[05 — Preparação do bastion e clonagem](05-bastion-git.md)

---

## 6.4 Trabalhar a partir do diretório Ansible

O arquivo `ansible.cfg` do projeto utiliza caminhos relativos.

Por isso, os comandos Ansible desta etapa devem ser executados a partir de:

```text
/home/student/rhcsa-ex200-v10-lab/ansible
```

Entre no diretório:

```bash
cd ~/rhcsa-ex200-v10-lab/ansible
```

Confira:

```bash
pwd
```

Resultado esperado:

```text
/home/student/rhcsa-ex200-v10-lab/ansible
```

Liste os principais arquivos:

```bash
find . -maxdepth 2 -type f | sort
```

---

## 6.5 Conferir o `ansible.cfg`

Exiba:

```bash
cat ansible.cfg
```

A versão atual do projeto utiliza:

```ini
[defaults]
inventory = ./inventory/hosts.yml
host_key_checking = True
retry_files_enabled = False
interpreter_python = auto_silent
forks = 10

[privilege_escalation]
become = False
```

### 6.5.1 `inventory`

```text
inventory = ./inventory/hosts.yml
```

Define o inventário padrão do projeto.

Por utilizar um caminho relativo, reforça a necessidade de executar os comandos a partir do diretório `ansible/`.

### 6.5.2 `host_key_checking`

```text
host_key_checking = True
```

A verificação de identidade SSH dos hosts permanece habilitada.

Não altere esta opção para `False` como forma de contornar erros de SSH.

Quando houver mudança legítima de host key, confirme a nova fingerprint diretamente no console da VM antes de atualizar `known_hosts`.

### 6.5.3 `interpreter_python`

```text
interpreter_python = auto_silent
```

Permite ao Ansible identificar automaticamente o interpretador Python apropriado nos hosts.

### 6.5.4 `forks`

```text
forks = 10
```

Define o limite de execuções paralelas.

O laboratório possui apenas três nós, portanto esse valor não implica a existência de dez VMs.

### 6.5.5 `become`

```text
become = False
```

A elevação de privilégios não é habilitada globalmente.

Os playbooks que precisam de privilégios administrativos declaram explicitamente:

```yaml
become: true
```

Essa separação é intencional.

---

## 6.6 Confirmar qual configuração o Ansible está utilizando

Execute:

```bash
ansible --version
```

Localize na saída a linha:

```text
config file = ...
```

Ela deve apontar para o `ansible.cfg` do projeto, por exemplo:

```text
/home/student/rhcsa-ex200-v10-lab/ansible/ansible.cfg
```

Uma validação objetiva pode ser feita com:

```bash
ansible-config dump --only-changed
```

Confirme especialmente:

```text
DEFAULT_HOST_LIST
HOST_KEY_CHECKING
INTERPRETER_PYTHON
```

Se o Ansible estiver utilizando outro arquivo de configuração, confirme o diretório atual e se existe uma variável `ANSIBLE_CONFIG` sobrescrevendo o projeto:

```bash
printf '%s\n' "${ANSIBLE_CONFIG:-<não definida>}"
```

---

## 6.7 Conferir o inventário

Exiba:

```bash
cat inventory/hosts.yml
```

A versão atual utiliza:

```yaml
---
all:
  children:

    control:
      hosts:
        bastion:
          ansible_connection: local
          ansible_python_interpreter: /usr/bin/python3

    managed:
      hosts:

        servera:
          ansible_host: 192.168.100.11

        serverb:
          ansible_host: 192.168.100.12

  vars:
    ansible_user: student
    ansible_ssh_private_key_file: /home/student/.ssh/id_ed25519_rhcsa_lab
```

O inventário pressupõe a arquitetura padrão documentada pelo projeto:

| Host | Grupo | Endereço |
|---|---|---|
| `bastion` | `control` | conexão local |
| `servera` | `managed` | `192.168.100.11` |
| `serverb` | `managed` | `192.168.100.12` |

Se você seguiu a documentação padrão, não é necessário alterar esses endereços.

---

## 6.8 Validar a sintaxe e a estrutura do inventário

Execute:

```bash
ansible-inventory --graph
```

A estrutura deve representar:

```text
@all:
  |--@control:
  |  |--bastion
  |--@managed:
  |  |--servera
  |  |--serverb
```

A apresentação exata pode variar conforme a versão do Ansible, mas os três hosts e os dois grupos precisam estar presentes.

Consulte também:

```bash
ansible-inventory --list
```

Para validar apenas `servera`:

```bash
ansible-inventory --host servera
```

Para `serverb`:

```bash
ansible-inventory --host serverb
```

Confira se os endereços correspondem a:

```text
servera = 192.168.100.11
serverb = 192.168.100.12
```

---

## 6.9 Confirmar a chave privada referenciada pelo inventário

O inventário utiliza:

```text
/home/student/.ssh/id_ed25519_rhcsa_lab
```

Confira:

```bash
ls -l /home/student/.ssh/id_ed25519_rhcsa_lab
```

Valide as permissões:

```bash
stat -c '%a %U:%G %n' \
  /home/student/.ssh/id_ed25519_rhcsa_lab
```

O arquivo deve pertencer a `student` e possuir permissão restrita.

Uma configuração típica é:

```text
600 student:student /home/student/.ssh/id_ed25519_rhcsa_lab
```

Não copie a chave privada para dentro do repositório.

---

## 6.10 Confirmar SSH antes de testar Ansible

O Ansible depende do SSH para `servera` e `serverb`.

Teste primeiro o mecanismo diretamente:

```bash
ssh -o BatchMode=yes servera hostname -f
```

Resultado esperado:

```text
servera.lab.test
```

Depois:

```bash
ssh -o BatchMode=yes serverb hostname -f
```

Resultado esperado:

```text
serverb.lab.test
```

Se um desses comandos falhar, corrija o SSH antes de diagnosticar o Ansible.

---

## 6.11 Confirmar as host keys conhecidas

Confira:

```bash
ssh-keygen -F servera
```

```bash
ssh-keygen -F serverb
```

Como `host_key_checking` está habilitado, as identidades corretas devem estar presentes em:

```text
/home/student/.ssh/known_hosts
```

Se uma host key tiver mudado porque uma VM foi recriada, valide a nova fingerprint pelo console da VM antes de substituir a entrada.

Não use:

```text
StrictHostKeyChecking=no
```

como correção permanente para o laboratório.

---

## 6.12 Preparar a elevação de privilégios da automação

Vários playbooks de preparação e limpeza utilizam:

```yaml
become: true
```

O runner atual do projeto executa esses playbooks sem solicitar senha de `sudo`.

Por isso, nas VMs **descartáveis e dedicadas ao laboratório**, o usuário `student` deve poder elevar privilégios sem interação.

Essa configuração não representa uma recomendação para servidores de produção.

### 6.12.1 Configurar no bastion

No `bastion`:

```bash
sudo visudo -f /etc/sudoers.d/rhcsa-lab-student
```

Adicione:

```sudoers
student ALL=(ALL) NOPASSWD: ALL
```

Salve e saia.

Ajuste:

```bash
sudo chmod 440 /etc/sudoers.d/rhcsa-lab-student
```

Valide:

```bash
sudo visudo -cf /etc/sudoers.d/rhcsa-lab-student
```

Resultado esperado:

```text
/etc/sudoers.d/rhcsa-lab-student: parsed OK
```

Teste sem prompt:

```bash
sudo -n true
```

O comando deve terminar com código `0` e sem solicitar senha.

Confira:

```bash
echo $?
```

Resultado esperado:

```text
0
```

### 6.12.2 Configurar em servera

Acesse:

```bash
ssh servera
```

Crie:

```bash
sudo visudo -f /etc/sudoers.d/rhcsa-lab-student
```

Conteúdo:

```sudoers
student ALL=(ALL) NOPASSWD: ALL
```

Depois:

```bash
sudo chmod 440 /etc/sudoers.d/rhcsa-lab-student
sudo visudo -cf /etc/sudoers.d/rhcsa-lab-student
sudo -n true
```

Saia:

```bash
exit
```

### 6.12.3 Configurar em serverb

Acesse:

```bash
ssh serverb
```

Repita:

```bash
sudo visudo -f /etc/sudoers.d/rhcsa-lab-student
```

Conteúdo:

```sudoers
student ALL=(ALL) NOPASSWD: ALL
```

Valide:

```bash
sudo chmod 440 /etc/sudoers.d/rhcsa-lab-student
sudo visudo -cf /etc/sudoers.d/rhcsa-lab-student
sudo -n true
```

Saia:

```bash
exit
```

---

## 6.13 Validar `sudo` não interativo a partir do bastion

No `bastion`, execute:

```bash
sudo -n true && echo "bastion: sudo OK"
```

Depois:

```bash
ssh servera 'sudo -n true' && echo "servera: sudo OK"
```

```bash
ssh serverb 'sudo -n true' && echo "serverb: sudo OK"
```

Resultados esperados:

```text
bastion: sudo OK
servera: sudo OK
serverb: sudo OK
```

Não prossiga se algum host solicitar senha.

---

## 6.14 Primeiro teste Ansible: grupo control

Ainda em:

```text
~/rhcsa-ex200-v10-lab/ansible
```

execute:

```bash
ansible control -m ansible.builtin.ping
```

O `bastion` deve retornar sucesso.

O módulo:

```text
ansible.builtin.ping
```

não executa ICMP.

Ele testa se o Ansible consegue executar código Python no host e receber uma resposta válida.

---

## 6.15 Testar os hosts gerenciados

Execute:

```bash
ansible managed -m ansible.builtin.ping
```

O resultado esperado para os dois hosts contém:

```text
SUCCESS
```

e:

```json
"ping": "pong"
```

Exemplo conceitual:

```text
servera | SUCCESS => {
    "changed": false,
    "ping": "pong"
}

serverb | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

Se `servera` ou `serverb` estiver `UNREACHABLE`, resolva o problema antes de prosseguir.

---

## 6.16 Testar todos os nós

Execute:

```bash
ansible all -m ansible.builtin.ping
```

Os três hosts devem responder:

```text
bastion
servera
serverb
```

com sucesso.

Esse teste valida:

- inventário;
- conexão local com `bastion`;
- SSH com os hosts gerenciados;
- chave privada;
- host keys;
- usuário remoto;
- disponibilidade do Python.

---

## 6.17 Confirmar a identidade dos hosts pelo Ansible

Execute:

```bash
ansible all \
  -m ansible.builtin.command \
  -a 'hostname -f'
```

Resultados esperados:

```text
bastion.lab.test
servera.lab.test
serverb.lab.test
```

Cada nome deve corresponder ao host do inventário que executou o comando.

Se `servera` retornar `serverb.lab.test`, por exemplo, interrompa a preparação e corrija a identidade da VM.

---

## 6.18 Confirmar o usuário remoto

Nos hosts gerenciados:

```bash
ansible managed \
  -m ansible.builtin.command \
  -a 'id -un'
```

Resultado esperado:

```text
student
```

---

## 6.19 Validar `become` pelo Ansible

Teste o grupo gerenciado:

```bash
ansible managed \
  --become \
  -m ansible.builtin.command \
  -a 'id -u'
```

Resultado esperado nos dois hosts:

```text
0
```

Teste o `bastion`:

```bash
ansible control \
  --become \
  -m ansible.builtin.command \
  -a 'id -u'
```

Resultado esperado:

```text
0
```

Se aparecer:

```text
Missing sudo password
```

ou uma falha de `sudo`, corrija a configuração `NOPASSWD` antes de continuar.

---

## 6.20 Verificar sintaxe dos playbooks principais

Antes da execução, valide os playbooks desta etapa.

Execute:

```bash
ansible-playbook \
  --syntax-check \
  playbooks/validate.yml
```

Depois:

```bash
ansible-playbook \
  --syntax-check \
  playbooks/00-bootstrap-dependencies.yml
```

E:

```bash
ansible-playbook \
  --syntax-check \
  playbooks/00-validate-dependencies.yml
```

Os três comandos devem terminar sem erro de sintaxe.

---

## 6.21 Validar o baseline de sistema operacional

Execute:

```bash
ansible-playbook playbooks/validate.yml
```

O playbook atual coleta fatos de todos os hosts e valida duas condições:

```text
ansible_distribution == "RedHat"
ansible_distribution_major_version == "9"
```

Portanto, o baseline local atual exige:

```text
Red Hat Enterprise Linux 9
```

nas três VMs.

A saída de sucesso apresenta informações como:

```text
inventory
fqdn
ipv4
python
```

e uma mensagem semelhante a:

```text
RedHat 9.x OK
```

### Importante sobre RHEL 10

O projeto utiliza RHEL 10 como referência para o objetivo de certificação e classificação de compatibilidade dos exercícios, mas o baseline local desta versão do repositório continua sendo RHEL 9.

Não altere `validate.yml` apenas para fazer uma VM incompatível passar na validação.

Uma futura migração do laboratório local para RHEL 10 deve incluir revisão dos exercícios, dependências e validações.

---

## 6.22 Inspecionar as dependências definidas pelo projeto

Exiba:

```bash
cat vars/lab_dependencies.yml
```

Esse arquivo divide as dependências em:

```text
control_plane_packages
managed_baseline_packages
control_plane_required_commands
managed_required_commands
```

A lista existe para que a infraestrutura necessária aos exercícios seja preparada antes do baseline.

Isso evita que o estudante precise instalar, durante um exercício, um pacote que deveria fazer parte da infraestrutura do próprio laboratório.

---

## 6.23 Preparar as dependências do laboratório

Antes desta etapa, confirme novamente que o `bastion` possui uma fonte funcional de pacotes:

```bash
sudo dnf repolist
```

O bootstrap utiliza os repositórios disponíveis no `bastion`.

Execute:

```bash
ansible-playbook \
  playbooks/00-bootstrap-dependencies.yml
```

### O que esse playbook faz

No grupo `control`, ele:

1. instala as dependências do plano de controle;
2. recria:

```text
/var/tmp/rhcsa-baseline-rpms
```

3. utiliza `dnf download --resolve --alldeps`;
4. constrói um conjunto local de RPMs necessários aos hosts gerenciados.

Depois, no grupo `managed`, ele:

1. cria um diretório temporário em cada host;
2. copia o conjunto de RPMs a partir do `bastion`;
3. instala os pacotes com os repositórios remotos desabilitados;
4. remove o diretório temporário das VMs gerenciadas.

Essa estratégia torna o `bastion` a fonte de preparação das dependências do laboratório.

### Requisito importante

O `bastion` precisa possuir repositórios capazes de fornecer os pacotes e suas dependências.

Se a tarefa de download falhar, corrija a origem de pacotes do `bastion` antes de prosseguir.

---

## 6.24 Validar o conjunto de dependências

Depois do bootstrap:

```bash
ansible-playbook \
  playbooks/00-validate-dependencies.yml
```

O playbook verifica comandos necessários tanto no plano de controle quanto nos hosts gerenciados.

Entre os recursos validados estão ferramentas relacionadas a:

```text
Git
SSH
arquivos e compressão
ACLs
atributos estendidos
SELinux
particionamento
LVM
XFS
ext4
NFS
AutoFS
chrony
firewalld
NetworkManager
Apache HTTP Server
```

Não substitua essa validação por uma checagem manual de apenas dois ou três comandos.

O playbook é a referência executável do baseline de dependências do projeto.

---

## 6.25 Executar novamente o teste de conectividade

Depois da instalação das dependências:

```bash
ansible all -m ansible.builtin.ping
```

Depois:

```bash
ansible all \
  -m ansible.builtin.command \
  -a 'hostname -f'
```

Isso confirma que a preparação não interrompeu a comunicação com nenhum nó.

---

## 6.26 Validar o CLI `lab`

Volte para a raiz:

```bash
cd ~/rhcsa-ex200-v10-lab
```

Confira a versão:

```bash
lab --version
```

Depois:

```bash
lab status
```

O comando consulta o inventário do projeto e executa `ansible.builtin.ping` nos nós.

Ele também verifica a presença local de:

```text
ansible
ssh
git
python3
```

O resultado esperado deve mostrar:

```text
Control Plane
  bastion      ...    ONLINE

Managed Nodes
  servera      ...    ONLINE
  serverb      ...    ONLINE
```

A seção de plataforma mostra o baseline local e o alvo de certificação:

```text
Local       RHEL 9.8
Exam target RHEL 10
```

A seção de ferramentas deve indicar:

```text
ansible    OK
ssh        OK
git        OK
python3    OK
```

Ao final:

```text
Environment: READY
```

---

## 6.27 Entender o que `lab status` valida

`lab status` é uma verificação rápida de saúde do ambiente.

Ele confirma principalmente:

- leitura do inventário;
- conectividade Ansible;
- Python nos nós;
- disponibilidade das ferramentas locais essenciais.

Porém:

```text
Environment: READY
```

não substitui:

```bash
ansible-playbook playbooks/validate.yml
```

nem:

```bash
ansible-playbook playbooks/00-validate-dependencies.yml
```

O primeiro valida o baseline de sistema operacional.

O segundo valida as dependências necessárias aos laboratórios.

Para considerar o ambiente pronto para o snapshot, **as três verificações devem estar corretas**.

---

## 6.28 Validar o catálogo de laboratórios

Execute:

```bash
lab list
```

O catálogo deve ser carregado sem erros de Python ou YAML.

Isso confirma que o CLI consegue descobrir os laboratórios presentes no repositório.

Não é necessário iniciar um exercício nesta etapa.

O primeiro laboratório será tratado depois da criação do baseline.

---

## 6.29 Verificação consolidada em sequência

Para uma conferência final, execute a partir do `bastion`.

Entre no diretório Ansible:

```bash
cd ~/rhcsa-ex200-v10-lab/ansible
```

Valide o inventário:

```bash
ansible-inventory --graph
```

Valide conectividade:

```bash
ansible all -m ansible.builtin.ping
```

Valide identidades:

```bash
ansible all \
  -m ansible.builtin.command \
  -a 'hostname -f'
```

Valide privilégios:

```bash
ansible all \
  --become \
  -m ansible.builtin.command \
  -a 'id -u'
```

Valide o sistema operacional:

```bash
ansible-playbook playbooks/validate.yml
```

Valide dependências:

```bash
ansible-playbook playbooks/00-validate-dependencies.yml
```

Volte à raiz:

```bash
cd ~/rhcsa-ex200-v10-lab
```

Valide o CLI:

```bash
lab status
```

E o catálogo:

```bash
lab list
```

---

## 6.30 Resultado mínimo esperado

O ambiente só deve seguir para o baseline quando:

```text
bastion   ONLINE
servera   ONLINE
serverb   ONLINE
```

e:

```text
Ansible ping       PASS
Hostname           correto
sudo/become        funcional
RHEL baseline      PASS
Dependências       PASS
lab status         READY
lab list           funcional
```

---

## 6.31 Problemas comuns

### `ansible-inventory` não encontra hosts

Confirme o diretório:

```bash
pwd
```

Esperado:

```text
/home/student/rhcsa-ex200-v10-lab/ansible
```

Confira:

```bash
cat ansible.cfg
```

E:

```bash
cat inventory/hosts.yml
```

Valide:

```bash
ansible-inventory --graph
```

---

### `ansible --version` mostra outro arquivo de configuração

Confira:

```bash
ansible --version
```

Depois:

```bash
printf '%s\n' "${ANSIBLE_CONFIG:-<não definida>}"
```

Entre novamente no diretório:

```bash
cd ~/rhcsa-ex200-v10-lab/ansible
```

Não altere o `ansible.cfg` do projeto apenas para esconder uma configuração externa incorreta.

---

### `UNREACHABLE` ou timeout

Teste primeiro a rede:

```bash
ping -c 2 servera
```

Depois:

```bash
ssh -o BatchMode=yes servera hostname -f
```

Confira:

```bash
ip route
```

No host de destino, verifique:

```bash
systemctl is-active sshd
```

e:

```bash
sudo firewall-cmd --list-services
```

Investigue rede, resolução de nomes e SSH antes de modificar o inventário.

---

### `Permission denied`

Confira a chave:

```bash
ls -l ~/.ssh/id_ed25519_rhcsa_lab
```

Confira a configuração efetiva:

```bash
ssh -G servera | grep -Ei '^(user|hostname|identityfile)'
```

Teste:

```bash
ssh -vvv servera
```

No destino:

```bash
ls -ld ~/.ssh
ls -l ~/.ssh/authorized_keys
```

---

### `Host key verification failed`

Não desabilite a verificação de host key.

Confirme a fingerprint no console do host de destino:

```bash
sudo ssh-keygen \
  -lf /etc/ssh/ssh_host_ed25519_key.pub
```

Somente depois de confirmar a identidade, remova uma entrada antiga do `known_hosts`.

---

### `ansible.builtin.ping` falha por Python

O módulo Ansible `ping` depende de Python no destino.

Confirme diretamente:

```bash
ssh servera 'python3 --version'
```

```bash
ssh serverb 'python3 --version'
```

Se estiver ausente, retorne à etapa 04 e corrija o baseline da VM.

---

### `Missing sudo password`

Isso significa que um playbook com `become: true` não conseguiu elevar privilégios sem interação.

Teste:

```bash
ssh servera 'sudo -n true'
```

```bash
ssh serverb 'sudo -n true'
```

E localmente:

```bash
sudo -n true
```

Confira:

```bash
sudo visudo -cf /etc/sudoers.d/rhcsa-lab-student
```

Não utilize `--ask-become-pass` como solução permanente para o runner desta versão do projeto.

---

### `validate.yml` rejeita o sistema operacional

O baseline atual exige:

```text
ansible_distribution == RedHat
ansible_distribution_major_version == 9
```

Confira:

```bash
ansible all \
  -m ansible.builtin.setup \
  -a 'filter=ansible_distribution*'
```

Não modifique o playbook apenas para transformar uma plataforma não validada em uma plataforma suportada.

---

### O bootstrap de dependências falha no `dnf download`

Confira no `bastion`:

```bash
sudo dnf repolist
```

Verifique:

```bash
command -v dnf
```

O playbook instala `dnf-plugins-core` no plano de controle, que fornece os recursos utilizados na preparação do conjunto de RPMs.

Confirme espaço:

```bash
df -h /var/tmp
```

Se o repositório local/DVD não possuir os pacotes requeridos, utilize uma fonte de pacotes compatível com o baseline.

---

### A validação de dependências informa `MISSING`

Leia o nome do comando apontado pelo playbook.

Consulte:

```bash
cat vars/lab_dependencies.yml
```

O arquivo define o baseline requerido.

Não remova um comando da lista apenas para fazer a validação passar sem entender qual exercício depende dele.

---

### `lab status` mostra `DEGRADED`

Execute manualmente:

```bash
cd ~/rhcsa-ex200-v10-lab/ansible
ansible all -m ansible.builtin.ping
```

Depois confira:

```bash
command -v ansible
command -v ssh
command -v git
command -v python3
```

`lab status` depende desses elementos.

---

### `lab status` mostra READY, mas `validate.yml` falha

Isso é possível.

`lab status` verifica conectividade e ferramentas essenciais.

`validate.yml` verifica o baseline de sistema operacional.

Resolva a falha do playbook antes de criar snapshots.

---

## 6.32 Critério para avançar

Antes de seguir para a criação do baseline e dos snapshots, confirme:

```text
[ ] execução feita a partir de bastion.lab.test
[ ] usuário student

[ ] ansible.cfg correto
[ ] inventário inventory/hosts.yml carregado
[ ] grupo control contém bastion
[ ] grupo managed contém servera e serverb

[ ] host_key_checking permanece habilitado
[ ] chave SSH dedicada existe e possui permissão correta
[ ] known_hosts contém as identidades validadas

[ ] SSH BatchMode funciona para servera
[ ] SSH BatchMode funciona para serverb

[ ] sudo -n funciona no bastion
[ ] sudo -n funciona no servera
[ ] sudo -n funciona no serverb

[ ] ansible control -m ping funciona
[ ] ansible managed -m ping funciona
[ ] ansible all -m ping funciona

[ ] hostnames retornados pelo Ansible estão corretos
[ ] become retorna UID 0 nos nós necessários

[ ] playbooks principais passam no syntax-check
[ ] playbooks/validate.yml passa
[ ] baseline local confirmado como RHEL 9

[ ] bootstrap de dependências foi concluído
[ ] playbooks/00-validate-dependencies.yml passa

[ ] lab --version funciona
[ ] lab status mostra Environment: READY
[ ] lab list carrega o catálogo
```

Com todos os itens atendidos, o ambiente está tecnicamente pronto para gerar um baseline consistente.

Continue para:

[07 — Baseline e snapshots](07-baseline.md)

[Índice](README.md) · [Home](../../README.md) · [Anterior](05-bastion-git.md) · [Próximo](07-baseline.md)
