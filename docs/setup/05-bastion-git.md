# 05 — Preparação do bastion e clonagem do projeto

[Índice](README.md) · [Home](../../README.md) · [Anterior](04-configuracao-vms.md) · [Próximo](06-validacao-ansible.md)

**Onde executar:** `bastion`, conectado como usuário `student`, exceto quando o texto indicar explicitamente outro local.

Esta etapa transforma o `bastion` na estação de controle do laboratório.

Ao final, o `bastion` deverá possuir:

- Git;
- Ansible Core;
- Python 3 e PyYAML;
- cliente OpenSSH;
- uma cópia limpa do projeto;
- uma chave SSH dedicada ao laboratório;
- acesso SSH não interativo a `servera` e `serverb`;
- o comando `lab` instalado no perfil do usuário `student`.

> Não execute a clonagem como `root`. O projeto foi estruturado para permanecer em `/home/student/rhcsa-ex200-v10-lab`.

---

## 5.1 Resultado esperado

A estrutura principal deverá ficar semelhante a:

```text
/home/student/
├── .local/
│   └── bin/
│       └── lab -> /home/student/rhcsa-ex200-v10-lab/bin/lab
├── .ssh/
│   ├── config
│   ├── id_ed25519_rhcsa_lab
│   ├── id_ed25519_rhcsa_lab.pub
│   └── known_hosts
└── rhcsa-ex200-v10-lab/
    ├── ansible/
    ├── bin/
    ├── bootstrap/
    ├── docs/
    ├── labctl/
    ├── labs/
    └── tests/
```

O fluxo de administração será:

```text
                       bastion
                 192.168.100.10
                        |
             Git + Ansible + lab CLI
                        |
              +---------+---------+
              |                   |
           SSH/Ansible         SSH/Ansible
              |                   |
           servera             serverb
       192.168.100.11      192.168.100.12
```

---

## 5.2 Confirmar que está no bastion

Antes de instalar qualquer componente:

```bash
hostname -f
```

Resultado esperado:

```text
bastion.lab.test
```

Confirme também o usuário:

```bash
id
```

O usuário esperado é:

```text
student
```

Confira o diretório pessoal:

```bash
printf '%s\n' "$HOME"
```

Resultado esperado:

```text
/home/student
```

Se esses valores não corresponderem ao ambiente esperado, não continue até identificar em qual máquina e usuário a sessão está sendo executada.

---

## 5.3 Validar rede e resolução de nomes

Antes de instalar dependências ou configurar SSH, confirme que o `bastion` alcança os dois hosts gerenciados.

Resolva os nomes:

```bash
getent hosts servera
```

```bash
getent hosts serverb
```

Resultados esperados:

```text
192.168.100.11  servera.lab.test servera
192.168.100.12  serverb.lab.test serverb
```

Teste a conectividade:

```bash
ping -c 2 servera
```

```bash
ping -c 2 serverb
```

A ausência de resposta ICMP não deve ser confundida com uma falha de SSH, mas neste laboratório os testes devem ser investigados antes de avançar.

Confira a porta 22:

```bash
timeout 5 bash -c '</dev/tcp/servera/22' && echo "servera: SSH acessível"
```

```bash
timeout 5 bash -c '</dev/tcp/serverb/22' && echo "serverb: SSH acessível"
```

Se algum teste falhar, retorne à etapa:

[04 — Configuração inicial das VMs](04-configuracao-vms.md)

---

## 5.4 Confirmar a origem de pacotes

Antes de instalar as ferramentas do `bastion`, confirme que o DNF possui uma origem funcional:

```bash
sudo dnf repolist
```

O comando deve apresentar repositórios habilitados, provenientes de:

- Red Hat Subscription Management; ou
- mídia DVD local configurada na etapa anterior.

Não avance se o `dnf` estiver sem uma origem válida de pacotes.

---

## 5.5 Instalar as dependências do bastion

Instale:

```bash
sudo dnf install -y \
  git \
  ansible-core \
  python3 \
  python3-pyyaml \
  openssh-clients
```

A instalação fornece as principais ferramentas utilizadas pelo projeto.

| Pacote | Finalidade |
|---|---|
| `git` | Clonar e atualizar o repositório |
| `ansible-core` | Preparar, restaurar e validar os cenários |
| `python3` | Executar o CLI e módulos Ansible |
| `python3-pyyaml` | Ler os arquivos YAML utilizados pelo projeto |
| `openssh-clients` | Acesso SSH aos hosts gerenciados |

---

## 5.6 Validar as dependências

Confira o Git:

```bash
git --version
```

Confira o Ansible:

```bash
ansible --version
```

Confira o Python:

```bash
python3 --version
```

Valide o módulo PyYAML:

```bash
python3 -c 'import yaml; print("PyYAML OK")'
```

Resultado esperado:

```text
PyYAML OK
```

Confira o cliente SSH:

```bash
ssh -V
```

Se algum comando não estiver disponível, resolva a instalação antes de continuar.

---

## 5.7 Confirmar que o diretório do projeto ainda não existe

O caminho esperado pelo projeto é:

```text
/home/student/rhcsa-ex200-v10-lab
```

Confira:

```bash
ls -ld ~/rhcsa-ex200-v10-lab 2>/dev/null || true
```

### Se o diretório não existir

Prossiga para a clonagem.

### Se o diretório já existir

Não execute `git clone` por cima dele.

Entre no diretório:

```bash
cd ~/rhcsa-ex200-v10-lab
```

Confira:

```bash
git status
```

```bash
git remote -v
```

```bash
git log -1 --oneline --decorate
```

Se houver alterações locais, preserve-as antes de qualquer atualização.

Este guia não orienta apagar alterações locais automaticamente.

---

## 5.8 Clonar o repositório público

Se o projeto ainda não existir no `bastion`, execute:

```bash
cd ~
```

Clone via HTTPS:

```bash
git clone https://github.com/eduardoandradej/rhcsa-ex200-v10-lab.git
```

Entre no diretório:

```bash
cd ~/rhcsa-ex200-v10-lab
```

O clone público via HTTPS não exige credenciais do GitHub para leitura.

Credenciais de GitHub somente são necessárias para operações de escrita, como `push`, e não fazem parte da preparação normal do estudante.

---

## 5.9 Validar a cópia do projeto

Confira o diretório atual:

```bash
pwd
```

Resultado esperado:

```text
/home/student/rhcsa-ex200-v10-lab
```

Confira o repositório remoto:

```bash
git remote -v
```

A origem deve apontar para:

```text
https://github.com/eduardoandradej/rhcsa-ex200-v10-lab.git
```

Confira a branch:

```bash
git branch --show-current
```

Confira o último commit:

```bash
git log -1 --oneline --decorate
```

Confira o estado da árvore:

```bash
git status
```

Em uma clonagem nova, o esperado é:

```text
nothing to commit, working tree clean
```

Também é útil identificar a versão ou tag associada ao commit atual:

```bash
git describe --tags --always
```

> A documentação do projeto evolui com o repositório. Quando estiver reproduzindo um ambiente específico, registre o commit ou a tag utilizada.

---

## 5.10 Conferir a estrutura essencial do repositório

No diretório do projeto:

```bash
find . -maxdepth 2 -type d \
  -not -path './.git*' \
  | sort
```

Confira especificamente:

```bash
test -d ansible && echo "ansible: OK"
test -d bootstrap && echo "bootstrap: OK"
test -d labctl && echo "labctl: OK"
test -d labs && echo "labs: OK"
test -d tests && echo "tests: OK"
test -f bin/lab && echo "bin/lab: OK"
```

Todos os itens devem existir.

Se algum deles estiver ausente em uma clonagem nova, confirme se o repositório correto foi clonado e se a operação terminou sem erros.

---

## 5.11 Separar a chave do laboratório das demais chaves SSH

O projeto utiliza uma chave SSH dedicada para o tráfego entre:

```text
bastion -> servera
bastion -> serverb
```

O arquivo utilizado pelo inventário atual é:

```text
/home/student/.ssh/id_ed25519_rhcsa_lab
```

Não reutilize uma chave pessoal do GitHub, de produção ou de outro ambiente.

Crie o diretório SSH, caso ainda não exista:

```bash
mkdir -p ~/.ssh
```

Ajuste a permissão:

```bash
chmod 700 ~/.ssh
```

---

## 5.12 Criar a chave SSH dedicada

Primeiro confira se a chave já existe:

```bash
ls -l ~/.ssh/id_ed25519_rhcsa_lab* 2>/dev/null || true
```

Se **não existir**, crie:

```bash
ssh-keygen \
  -t ed25519 \
  -f ~/.ssh/id_ed25519_rhcsa_lab \
  -C rhcsa-lab
```

O `ssh-keygen` solicitará uma passphrase.

Para um laboratório automatizado, o usuário pode optar por uma chave sem passphrase ou utilizar `ssh-agent`.

O projeto não armazena nem distribui a chave privada.

### Permissões esperadas

Ajuste:

```bash
chmod 600 ~/.ssh/id_ed25519_rhcsa_lab
chmod 644 ~/.ssh/id_ed25519_rhcsa_lab.pub
```

Confira:

```bash
ls -l ~/.ssh/id_ed25519_rhcsa_lab*
```

A chave privada deve ser legível apenas pelo proprietário.

---

## 5.13 Conferir a fingerprint da chave do bastion

Execute:

```bash
ssh-keygen -lf ~/.ssh/id_ed25519_rhcsa_lab.pub
```

Esse valor identifica a chave pública utilizada pelo `bastion` para autenticação nos hosts gerenciados.

Ele não é a mesma coisa que a fingerprint da **host key** de `servera` ou `serverb`.

---

## 5.14 Validar as fingerprints de servera e serverb antes do primeiro acesso

Na primeira conexão SSH, o cliente perguntará se a identidade do host deve ser aceita.

Não aceite automaticamente sem saber qual máquina está sendo acessada.

### Em servera

Pelo console de `servera`, execute:

```bash
sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

Anote a fingerprint.

### Em serverb

Pelo console de `serverb`:

```bash
sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

Anote a fingerprint.

As duas fingerprints devem ser diferentes.

Esses valores serão comparados com o aviso apresentado pelo cliente SSH no `bastion`.

---

## 5.15 Copiar a chave pública para servera

De volta ao `bastion`:

```bash
ssh-copy-id \
  -i ~/.ssh/id_ed25519_rhcsa_lab.pub \
  student@servera
```

Na primeira conexão, compare a fingerprint apresentada pelo SSH com a fingerprint obtida diretamente no console de `servera`.

Somente depois de confirmar a identidade do host, aceite a chave.

O comando solicitará a senha atual do usuário `student` em `servera`.

Ele copia **somente a chave pública**.

A chave privada permanece no `bastion`.

---

## 5.16 Copiar a chave pública para serverb

Execute:

```bash
ssh-copy-id \
  -i ~/.ssh/id_ed25519_rhcsa_lab.pub \
  student@serverb
```

Novamente, confira a fingerprint de `serverb` antes de aceitar a host key.

---

## 5.17 Validar o `authorized_keys` nos hosts gerenciados

Em `servera`, pelo console ou SSH:

```bash
ls -ld ~/.ssh
```

```bash
ls -l ~/.ssh/authorized_keys
```

Permissões recomendadas:

```text
~/.ssh                  700
~/.ssh/authorized_keys  600
```

Se necessário:

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

Repita em `serverb`.

---

## 5.18 Criar a configuração SSH do bastion

No `bastion`, crie ou edite:

```bash
nano ~/.ssh/config
```

Adicione:

```sshconfig
Host servera
    HostName 192.168.100.11
    User student
    IdentityFile ~/.ssh/id_ed25519_rhcsa_lab
    IdentitiesOnly yes

Host serverb
    HostName 192.168.100.12
    User student
    IdentityFile ~/.ssh/id_ed25519_rhcsa_lab
    IdentitiesOnly yes
```

Salve o arquivo.

Ajuste:

```bash
chmod 600 ~/.ssh/config
```

Confira:

```bash
ls -l ~/.ssh/config
```

---

## 5.19 Entender por que `IdentitiesOnly yes` é utilizado

Um usuário pode possuir várias chaves carregadas no `ssh-agent` ou no diretório `~/.ssh`.

A diretiva:

```text
IdentitiesOnly yes
```

faz o cliente SSH utilizar explicitamente a chave configurada para o laboratório, reduzindo tentativas com identidades que pertencem a outros ambientes.

Isso ajuda a manter o laboratório isolado de:

- chaves pessoais;
- credenciais de GitHub;
- chaves corporativas;
- outros ambientes de estudo.

---

## 5.20 Validar acesso SSH explícito

Antes de depender do arquivo `~/.ssh/config`, teste a chave diretamente.

Para `servera`:

```bash
ssh \
  -i ~/.ssh/id_ed25519_rhcsa_lab \
  student@servera \
  hostname -f
```

Resultado esperado:

```text
servera.lab.test
```

Para `serverb`:

```bash
ssh \
  -i ~/.ssh/id_ed25519_rhcsa_lab \
  student@serverb \
  hostname -f
```

Resultado esperado:

```text
serverb.lab.test
```

---

## 5.21 Validar acesso pelo arquivo `~/.ssh/config`

Agora teste:

```bash
ssh servera hostname -f
```

Resultado esperado:

```text
servera.lab.test
```

Depois:

```bash
ssh serverb hostname -f
```

Resultado esperado:

```text
serverb.lab.test
```

---

## 5.22 Validar SSH não interativo

O Ansible e o CLI do laboratório precisam conectar sem solicitar senha de login.

Teste:

```bash
ssh \
  -o BatchMode=yes \
  -o ConnectTimeout=5 \
  servera \
  hostname -f
```

Depois:

```bash
ssh \
  -o BatchMode=yes \
  -o ConnectTimeout=5 \
  serverb \
  hostname -f
```

Os dois comandos devem terminar sem prompt de senha.

Resultados esperados:

```text
servera.lab.test
```

e:

```text
serverb.lab.test
```

Se `BatchMode=yes` falhar, não avance para o Ansible.

---

## 5.23 Verificar as host keys armazenadas

Depois das primeiras conexões:

```bash
ssh-keygen -F servera
```

```bash
ssh-keygen -F serverb
```

Também pode conferir:

```bash
ls -l ~/.ssh/known_hosts
```

O projeto mantém verificação de host key habilitada no Ansible.

Por isso, `known_hosts` deve refletir as identidades corretas de `servera` e `serverb`.

---

## 5.24 O que fazer se uma host key mudar

Uma mudança de host key pode acontecer legitimamente quando:

- uma VM é reinstalada;
- uma VM é recriada a partir de template;
- um snapshot anterior é restaurado;
- as SSH host keys são regeneradas.

Também pode indicar que o cliente está alcançando um sistema diferente do esperado.

Por isso, não remova o aviso indiscriminadamente.

Primeiro confirme a nova fingerprint diretamente no console da VM:

```bash
sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

Somente depois de confirmar a identidade, remova a entrada antiga.

Exemplo para `servera`:

```bash
ssh-keygen -R servera
```

Se houver uma entrada pelo endereço IP:

```bash
ssh-keygen -R 192.168.100.11
```

Depois faça uma nova conexão e valide a fingerprint novamente.

Repita o procedimento correspondente para `serverb`, se necessário.

---

## 5.25 Se a chave utilizar passphrase

Caso a chave dedicada tenha sido criada com passphrase, utilize `ssh-agent`.

Inicie o agente, se necessário:

```bash
eval "$(ssh-agent -s)"
```

Carregue a chave:

```bash
ssh-add ~/.ssh/id_ed25519_rhcsa_lab
```

Confira:

```bash
ssh-add -l
```

Depois repita:

```bash
ssh -o BatchMode=yes servera hostname -f
ssh -o BatchMode=yes serverb hostname -f
```

O agente vale para a sessão em que foi iniciado.

---

## 5.26 Instalar o comando `lab`

Entre na raiz do projeto:

```bash
cd ~/rhcsa-ex200-v10-lab
```

Execute o instalador fornecido pelo próprio repositório:

```bash
bash bootstrap/10-install-lab-cli.sh
```

O script valida a presença de:

```text
python3
ansible
ssh
PyYAML
```

e cria um link para o CLI em:

```text
~/.local/bin/lab
```

---

## 5.27 Atualizar o `PATH`

O instalador acrescenta ao `~/.bashrc`, quando necessário:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Recarregue o perfil:

```bash
source ~/.bashrc
```

Confira:

```bash
command -v lab
```

Resultado esperado:

```text
/home/student/.local/bin/lab
```

Confira o link:

```bash
readlink -f ~/.local/bin/lab
```

Ele deve resolver para:

```text
/home/student/rhcsa-ex200-v10-lab/bin/lab
```

---

## 5.28 Validar o CLI

Confira a versão:

```bash
lab --version
```

Liste os laboratórios:

```bash
lab list
```

O comando deve exibir o catálogo disponível no repositório sem erro de Python, YAML ou PATH.

A validação completa do ambiente será executada na próxima etapa.

---

## 5.29 Não copiar credenciais para o repositório

O diretório do projeto não deve receber:

```text
chaves SSH privadas
authorized_keys pessoais
tokens do GitHub
senhas
activation keys
arquivos de assinatura Red Hat
credenciais de nuvem
arquivos .env com segredos
```

A chave privada do laboratório deve permanecer somente em:

```text
/home/student/.ssh/id_ed25519_rhcsa_lab
```

Nunca copie essa chave para dentro de:

```text
/home/student/rhcsa-ex200-v10-lab
```

Antes de qualquer contribuição futura para o Git, confira os arquivos que serão adicionados ao commit.

---

## 5.30 Atualizar uma instalação existente do projeto

Esta subseção só se aplica quando o repositório já foi clonado anteriormente.

Entre no diretório:

```bash
cd ~/rhcsa-ex200-v10-lab
```

Confira alterações locais:

```bash
git status
```

Se a árvore estiver limpa:

```bash
git fetch --tags origin
```

Confira:

```bash
git log --oneline --decorate HEAD..origin/main
```

Se desejar atualizar a branch `main` e não houver alterações locais:

```bash
git switch main
```

```bash
git pull --ff-only
```

O uso de `--ff-only` impede que um `pull` crie um merge inesperado.

Se existirem alterações locais, não execute comandos de atualização destrutivos. Preserve ou versione o trabalho antes de sincronizar.

---

## 5.31 Uso do GitHub para estudantes e mantenedores

Para **utilizar os laboratórios**, basta o clone público via HTTPS:

```text
https://github.com/eduardoandradej/rhcsa-ex200-v10-lab.git
```

Não é necessário possuir credenciais de escrita no GitHub.

Operações como:

```text
git push
criação de branches remotas
pull requests
manutenção do projeto
```

fazem parte do fluxo de contribuição e não são requisito para executar os laboratórios.

As credenciais utilizadas para contribuir com o GitHub devem permanecer separadas da chave:

```text
id_ed25519_rhcsa_lab
```

que existe exclusivamente para comunicação entre as VMs do laboratório.

---

## 5.32 Validação consolidada

No `bastion`, execute:

```bash
hostname -f
```

Esperado:

```text
bastion.lab.test
```

Confira Git:

```bash
git --version
```

Confira Ansible:

```bash
ansible --version
```

Confira Python e PyYAML:

```bash
python3 -c 'import sys, yaml; print(sys.version.split()[0]); print("PyYAML OK")'
```

Confira o projeto:

```bash
cd ~/rhcsa-ex200-v10-lab
git status
git log -1 --oneline --decorate
```

Confira SSH:

```bash
ssh -o BatchMode=yes servera hostname -f
ssh -o BatchMode=yes serverb hostname -f
```

Confira o CLI:

```bash
lab --version
lab list
```

---

## 5.33 Problemas comuns

### `git clone` retorna que o diretório já existe

Não clone por cima.

Confira:

```bash
cd ~/rhcsa-ex200-v10-lab
git status
git remote -v
```

Decida se a cópia existente deve ser atualizada ou preservada.

### `dnf` não encontra `ansible-core`

Confira:

```bash
sudo dnf repolist
```

Retorne à configuração de repositórios da etapa 04.

Não substitua o problema instalando pacotes de fontes aleatórias.

### `python3 -c 'import yaml'` falha

Confira:

```bash
rpm -q python3-pyyaml
```

Instale, se necessário:

```bash
sudo dnf install -y python3-pyyaml
```

### `ssh-copy-id` solicita senha repetidamente

Confirme no host de destino:

```bash
id student
```

```bash
systemctl is-active sshd
```

Confira também se autenticação compatível com o primeiro provisionamento está disponível.

Se necessário, use o console da VM para investigar antes de alterar a configuração do SSH.

### `Permission denied (publickey,password)`

No `bastion`:

```bash
ls -l ~/.ssh/id_ed25519_rhcsa_lab*
```

Confirme a chave configurada:

```bash
ssh -G servera | grep -i '^identityfile'
```

No destino:

```bash
ls -ld ~/.ssh
ls -l ~/.ssh/authorized_keys
```

### `Host key verification failed`

Não desabilite a verificação de host key.

Primeiro confirme a fingerprint no console do servidor.

Depois corrija somente a entrada correspondente em `known_hosts`.

### `ssh -o BatchMode=yes` solicita interação ou falha

Isso indica que o acesso ainda não está pronto para Ansible.

Teste detalhadamente:

```bash
ssh -vvv servera
```

Use a saída para identificar:

- chave selecionada;
- arquivo de configuração utilizado;
- host key;
- método de autenticação.

### `lab: command not found`

Confira:

```bash
ls -l ~/.local/bin/lab
```

Depois:

```bash
printf '%s\n' "$PATH" | tr ':' '\n'
```

Recarregue:

```bash
source ~/.bashrc
```

Confira novamente:

```bash
command -v lab
```

### `lab` apresenta erro de PyYAML

Valide:

```bash
python3 -c 'import yaml; print(yaml.__version__)'
```

Se falhar:

```bash
sudo dnf install -y python3-pyyaml
```

### O clone foi feito como `root`

Não continue utilizando uma cópia em `/root`.

O projeto é esperado em:

```text
/home/student/rhcsa-ex200-v10-lab
```

Faça a clonagem como `student`.

---

## 5.34 Critério para avançar

Antes de seguir para a validação do Ansible, confirme:

```text
[ ] sessão executada em bastion.lab.test
[ ] usuário atual é student

[ ] Git instalado
[ ] Ansible Core instalado
[ ] Python 3 instalado
[ ] PyYAML funcionando
[ ] cliente OpenSSH instalado

[ ] projeto clonado em /home/student/rhcsa-ex200-v10-lab
[ ] origin aponta para o repositório correto
[ ] working tree está em estado conhecido

[ ] chave ~/.ssh/id_ed25519_rhcsa_lab existe
[ ] chave privada possui permissão restrita
[ ] chave pública foi instalada em servera
[ ] chave pública foi instalada em serverb

[ ] fingerprint de servera foi validada
[ ] fingerprint de serverb foi validada
[ ] host keys corretas estão em known_hosts

[ ] ssh servera funciona
[ ] ssh serverb funciona
[ ] BatchMode funciona sem senha em servera
[ ] BatchMode funciona sem senha em serverb

[ ] comando lab está em ~/.local/bin
[ ] lab --version funciona
[ ] lab list funciona
```

Com esses requisitos atendidos, prossiga para:

[06 — Configuração e validação do Ansible](06-validacao-ansible.md)

[Índice](README.md) · [Home](../../README.md) · [Anterior](04-configuracao-vms.md) · [Próximo](06-validacao-ansible.md)
