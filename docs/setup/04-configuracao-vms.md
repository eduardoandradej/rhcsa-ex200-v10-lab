# 04 — Configuração inicial das VMs

[Índice](README.md) · [Home](../../README.md) · [Anterior](03-criacao-vms.md) · [Próximo](05-bastion-git.md)

**Onde executar:** principalmente no console de cada VM, como `student` com `sudo`.

Esta etapa é comum aos dois métodos de criação das máquinas virtuais:

- **Método A — instalação manual a partir da ISO do RHEL**;
- **Método B — implantação a partir da imagem-base QCOW2**.

Os dois métodos devem chegar aqui com as três VMs existentes no libvirt:

```text
bastion
servera
serverb
```

O objetivo desta etapa é transformar essas VMs em um ambiente consistente, com identidade, rede, resolução de nomes, SSH, firewall, SELinux e acesso a pacotes corretamente configurados.

---

## 4.1 Resultado esperado

Ao final desta etapa:

| VM | Hostname | IPv4 |
|---|---|---|
| `bastion` | `bastion.lab.test` | `192.168.100.10/24` |
| `servera` | `servera.lab.test` | `192.168.100.11/24` |
| `serverb` | `serverb.lab.test` | `192.168.100.12/24` |

Parâmetros comuns:

```text
Gateway:     192.168.100.1
DNS:         192.168.100.1
Domínio:     lab.test
Rede:        192.168.100.0/24
```

Também devem estar funcionando:

```text
student
sudo
sshd
firewalld
SELinux Enforcing
dnf
resolução de nomes entre as VMs
```

---

## 4.2 Antes de alterar a rede

A mudança de DHCP para endereço estático pode interromper uma sessão SSH em andamento.

Por isso, faça a configuração inicial de rede preferencialmente pelo:

- console da VM no Cockpit;
- `virt-manager`;
- `virt-viewer`;
- outro console local fornecido pelo libvirt.

Evite depender exclusivamente do SSH enquanto altera o perfil de rede.

Em cada VM, confirme o estado atual:

```bash
hostnamectl
```

```bash
ip -br address
```

```bash
ip route
```

```bash
nmcli device status
```

```bash
nmcli connection show
```

---

## 4.3 Identificar o perfil de rede correto

Não suponha que a interface seja `eth0` nem que o perfil tenha um nome específico.

Primeiro identifique:

```bash
nmcli -f NAME,UUID,TYPE,DEVICE connection show
```

Exemplo:

```text
NAME                UUID                                  TYPE      DEVICE
Wired connection 1  xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx  ethernet  enp1s0
```

O nome da interface pode variar entre instalações.

O importante é identificar o **perfil ativo ligado à interface conectada à rede `rhcsa-lab`**.

Nos exemplos abaixo, substitua:

```text
NOME_DA_CONEXAO
```

pelo nome real mostrado por `nmcli`.

---

## 4.4 Configurar o bastion

Entre no console do `bastion`.

### 4.4.1 Definir o hostname

```bash
sudo hostnamectl set-hostname bastion.lab.test
```

Confira:

```bash
hostnamectl
```

### 4.4.2 Identificar o perfil de rede

```bash
nmcli connection show
```

Defina uma variável com o nome real do perfil.

Exemplo:

```bash
LAB_CONNECTION='Wired connection 1'
```

Confirme:

```bash
printf '%s\n' "$LAB_CONNECTION"
```

### 4.4.3 Configurar IPv4 estático

```bash
sudo nmcli connection modify "$LAB_CONNECTION" \
  ipv4.method manual \
  ipv4.addresses 192.168.100.10/24 \
  ipv4.gateway 192.168.100.1 \
  ipv4.dns 192.168.100.1 \
  ipv4.dns-search lab.test \
  connection.autoconnect yes
```

Reative o perfil:

```bash
sudo nmcli connection up "$LAB_CONNECTION"
```

### 4.4.4 Validar

```bash
hostname -f
```

```bash
ip -4 -br address
```

```bash
ip route
```

O endereço esperado é:

```text
192.168.100.10/24
```

---

## 4.5 Configurar o servera

Entre no console do `servera`.

### 4.5.1 Definir o hostname

```bash
sudo hostnamectl set-hostname servera.lab.test
```

### 4.5.2 Identificar o perfil

```bash
nmcli connection show
```

Defina a variável com o nome real.

Exemplo:

```bash
LAB_CONNECTION='Wired connection 1'
```

### 4.5.3 Configurar IPv4 estático

```bash
sudo nmcli connection modify "$LAB_CONNECTION" \
  ipv4.method manual \
  ipv4.addresses 192.168.100.11/24 \
  ipv4.gateway 192.168.100.1 \
  ipv4.dns 192.168.100.1 \
  ipv4.dns-search lab.test \
  connection.autoconnect yes
```

Reative:

```bash
sudo nmcli connection up "$LAB_CONNECTION"
```

### 4.5.4 Validar

```bash
hostname -f
ip -4 -br address
ip route
```

O endereço esperado é:

```text
192.168.100.11/24
```

---

## 4.6 Configurar o serverb

Entre no console do `serverb`.

### 4.6.1 Definir o hostname

```bash
sudo hostnamectl set-hostname serverb.lab.test
```

### 4.6.2 Identificar o perfil

```bash
nmcli connection show
```

Defina a variável com o nome real.

Exemplo:

```bash
LAB_CONNECTION='Wired connection 1'
```

### 4.6.3 Configurar IPv4 estático

```bash
sudo nmcli connection modify "$LAB_CONNECTION" \
  ipv4.method manual \
  ipv4.addresses 192.168.100.12/24 \
  ipv4.gateway 192.168.100.1 \
  ipv4.dns 192.168.100.1 \
  ipv4.dns-search lab.test \
  connection.autoconnect yes
```

Reative:

```bash
sudo nmcli connection up "$LAB_CONNECTION"
```

### 4.6.4 Validar

```bash
hostname -f
ip -4 -br address
ip route
```

O endereço esperado é:

```text
192.168.100.12/24
```

---

## 4.7 Configurar resolução local de nomes

Mesmo com o DNS fornecido pelo libvirt, este laboratório mantém uma tabela local explícita para tornar a resolução entre as VMs previsível.

Em **cada uma das três VMs**, edite:

```bash
sudoedit /etc/hosts
```

Preserve as entradas de `localhost`.

Adicione uma única vez:

```text
192.168.100.10 bastion.lab.test bastion
192.168.100.11 servera.lab.test servera
192.168.100.12 serverb.lab.test serverb
```

Não duplique essas entradas.

### 4.7.1 Validar a resolução

Em cada VM:

```bash
getent hosts bastion
getent hosts servera
getent hosts serverb
```

Exemplo esperado:

```text
192.168.100.11  servera.lab.test servera
```

Também confira o FQDN local:

```bash
hostname -f
```

---

## 4.8 Validar identidades individuais das VMs

Esta validação é especialmente importante quando o ambiente foi criado pelo **Método B**.

Em cada VM:

```bash
cat /etc/machine-id
```

Os valores de `bastion`, `servera` e `serverb` devem ser diferentes.

Não avance se duas VMs apresentarem o mesmo `machine-id`.

### 4.8.1 Validar as SSH host keys

Em cada VM:

```bash
sudo ls -l /etc/ssh/ssh_host_*
```

Confira a fingerprint da chave ED25519:

```bash
sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

As três VMs devem possuir fingerprints diferentes.

Se uma VM não possuir SSH host keys:

```bash
sudo ssh-keygen -A
```

Depois:

```bash
sudo systemctl restart sshd
```

---

## 4.9 Validar o usuário `student`

O projeto utiliza o usuário:

```text
student
```

em todas as VMs.

Confira:

```bash
id student
```

O usuário deve existir e pertencer ao grupo administrativo `wheel`.

Exemplo:

```text
groups=...,wheel
```

Se o usuário ainda não existir:

```bash
sudo useradd -m -G wheel student
```

Defina uma senha local:

```bash
sudo passwd student
```

Se o usuário já existir, não o recrie.

Confira o acesso ao `sudo`:

```bash
sudo -v
```

A configuração `NOPASSWD` necessária para a automação dos laboratórios será tratada posteriormente, na etapa de validação do Ansible.

Não publique senhas locais no repositório Git.

---

## 4.10 Habilitar SSH

Em cada VM:

```bash
sudo systemctl enable --now sshd
```

Confira:

```bash
systemctl is-active sshd
```

Resultado esperado:

```text
active
```

Confira também:

```bash
ss -lnt | grep ':22'
```

---

## 4.11 Manter SELinux habilitado

Este laboratório utiliza SELinux como parte dos exercícios RHCSA.

Confira:

```bash
getenforce
```

Resultado esperado:

```text
Enforcing
```

Se o resultado for `Permissive` ou `Disabled`, investigue a configuração antes de continuar.

O laboratório não deve ser preparado desabilitando SELinux para contornar problemas.

Confira também:

```bash
sestatus
```

---

## 4.12 Habilitar e configurar o firewalld

Em cada VM:

```bash
sudo systemctl enable --now firewalld
```

Confira:

```bash
systemctl is-active firewalld
```

Autorize SSH:

```bash
sudo firewall-cmd --permanent --add-service=ssh
```

Recarregue:

```bash
sudo firewall-cmd --reload
```

Valide:

```bash
sudo firewall-cmd --list-services
```

O serviço `ssh` deve aparecer na zona efetivamente utilizada pela interface.

Confira a zona ativa:

```bash
sudo firewall-cmd --get-active-zones
```

Não desabilite o firewall para simplificar o laboratório.

---

## 4.13 Escolher a origem dos pacotes RHEL

As três VMs precisam de uma origem funcional de pacotes para que as etapas seguintes possam instalar dependências.

Utilize **uma fonte coerente com sua instalação**.

As opções documentadas são:

1. Red Hat Subscription Management;
2. mídia DVD local compatível com a versão instalada.

Não misture repositórios de versões diferentes do RHEL.

---

## 4.14 Opção A — Red Hat Subscription Management

Use esta opção quando as VMs puderem ser registradas individualmente por meio de uma assinatura ou acesso autorizado.

### 4.14.1 Verificar o estado atual

Em cada VM:

```bash
sudo subscription-manager identity
```

Se o sistema ainda não estiver registrado, o comando informará que não existe identidade válida.

### 4.14.2 Registrar a VM

Execute de forma interativa:

```bash
sudo subscription-manager register
```

Não armazene usuário, senha, activation key ou token em arquivos versionados pelo projeto.

### 4.14.3 Confirmar a identidade

```bash
sudo subscription-manager identity
```

Se estiver utilizando o Método B, cada VM deve possuir sua própria identidade.

Nunca registre a imagem-base que será utilizada como template.

### 4.14.4 Conferir repositórios

```bash
sudo dnf repolist
```

Confirme que há repositórios adequados à versão instalada antes de prosseguir.

---

## 4.15 Opção B — repositório local pela ISO/DVD

Esta opção utiliza a mídia DVD correspondente à mesma versão do RHEL instalada na VM.

### 4.15.1 Método A

Quando as VMs foram instaladas pela ISO, o CD-ROM virtual pode já estar associado à máquina.

Confira:

```bash
lsblk
```

O dispositivo costuma aparecer como:

```text
sr0
```

mas o nome deve ser validado no seu sistema.

### 4.15.2 Método B

As VMs criadas pela imagem-base não precisam ter um CD-ROM virtual conectado.

Se você optar pelo repositório local, anexe uma ISO oficial e compatível à VM antes de continuar.

Essa ação deve ser feita no **host KVM**, pelo Cockpit, `virt-manager` ou libvirt.

Depois retorne ao console da VM e confirme:

```bash
lsblk
```

### 4.15.3 Montar a mídia

Em cada VM que utilizar o DVD:

```bash
sudo mkdir -p /mnt/rhel-dvd
```

Monte somente leitura:

```bash
sudo mount -o ro /dev/sr0 /mnt/rhel-dvd
```

Valide a estrutura:

```bash
ls /mnt/rhel-dvd/BaseOS/repodata
```

```bash
ls /mnt/rhel-dvd/AppStream/repodata
```

Os dois caminhos devem existir.

### 4.15.4 Configurar montagem persistente

Após confirmar que `/dev/sr0` é realmente o dispositivo correto, adicione uma única entrada a `/etc/fstab`:

```text
/dev/sr0 /mnt/rhel-dvd iso9660 ro,nofail 0 0
```

Não duplique a entrada.

Teste:

```bash
sudo umount /mnt/rhel-dvd
sudo mount -a
```

Confirme:

```bash
mount | grep '/mnt/rhel-dvd'
```

### 4.15.5 Criar os repositórios locais

Crie:

```bash
sudoedit /etc/yum.repos.d/rhcsa-dvd.repo
```

Conteúdo:

```ini
[rhcsa-dvd-baseos]
name=RHCSA DVD BaseOS
baseurl=file:///mnt/rhel-dvd/BaseOS
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release

[rhcsa-dvd-appstream]
name=RHCSA DVD AppStream
baseurl=file:///mnt/rhel-dvd/AppStream
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
```

Confira se a chave indicada existe:

```bash
ls -l /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
```

Atualize o cache:

```bash
sudo dnf clean all
```

```bash
sudo dnf repolist
```

Os repositórios locais devem aparecer habilitados.

> O DVD fornece os pacotes existentes na mídia. Ele não substitui os repositórios de atualização da Red Hat.

---

## 4.16 Instalar o conjunto básico de pacotes

Com uma fonte de pacotes funcional, instale em cada VM:

```bash
sudo dnf install -y \
  openssh-server \
  openssh-clients \
  python3 \
  tar \
  gzip \
  bzip2 \
  xz \
  unzip \
  zip
```

Valide:

```bash
python3 --version
```

```bash
ssh -V
```

```bash
tar --version | head -1
```

O `python3` é necessário para a execução dos módulos Ansible nas VMs gerenciadas.

---

## 4.17 Validar conectividade com o gateway

Em cada VM:

```bash
ping -c 2 192.168.100.1
```

A resposta do gateway confirma conectividade básica com a bridge da rede `rhcsa-lab`.

Um ping bem-sucedido, porém, não substitui os testes de resolução de nomes e SSH.

---

## 4.18 Validar comunicação entre as VMs

No `bastion`:

```bash
getent hosts servera
getent hosts serverb
```

Teste conectividade IP:

```bash
ping -c 2 servera
```

```bash
ping -c 2 serverb
```

Teste a porta SSH:

```bash
ssh -o ConnectTimeout=5 student@servera
```

Na primeira conexão, confira a fingerprint do host antes de aceitar.

Saia:

```bash
exit
```

Repita:

```bash
ssh -o ConnectTimeout=5 student@serverb
```

Saia:

```bash
exit
```

A autenticação automatizada por chave será configurada na etapa seguinte.

---

## 4.19 Validar a topologia dos discos

Os discos adicionais fazem parte dos exercícios e não devem ser utilizados durante a preparação inicial.

### 4.19.1 bastion

```bash
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS
```

Esperado:

```text
vda   30G
```

### 4.19.2 servera

```bash
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS
```

Esperado:

```text
vda   30G
vdb    5G
vdc    5G
vdd    3G
vde    2G
```

Os discos `vdb`, `vdc`, `vdd` e `vde` devem estar disponíveis para os laboratórios.

### 4.19.3 serverb

```bash
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS
```

Esperado:

```text
vda   30G
vdb    5G
vdc    3G
```

Os discos adicionais não devem estar montados nem conter estruturas criadas durante a preparação do ambiente.

---

## 4.20 Validação consolidada por VM

Em cada máquina, execute:

```bash
hostname -f
```

```bash
ip -4 -br address
```

```bash
ip route
```

```bash
getenforce
```

```bash
systemctl is-active sshd
```

```bash
systemctl is-active firewalld
```

```bash
sudo firewall-cmd --get-active-zones
```

```bash
sudo firewall-cmd --list-services
```

```bash
dnf repolist
```

```bash
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS
```

---

## 4.21 Valores esperados

### bastion

```text
Hostname:  bastion.lab.test
IPv4:      192.168.100.10/24
Gateway:   192.168.100.1
SELinux:   Enforcing
SSH:       active
Firewall:  active
```

### servera

```text
Hostname:  servera.lab.test
IPv4:      192.168.100.11/24
Gateway:   192.168.100.1
SELinux:   Enforcing
SSH:       active
Firewall:  active
```

### serverb

```text
Hostname:  serverb.lab.test
IPv4:      192.168.100.12/24
Gateway:   192.168.100.1
SELinux:   Enforcing
SSH:       active
Firewall:  active
```

---

## 4.22 Problemas comuns

### `nmcli connection up` interrompeu o acesso

Isso pode acontecer ao trocar DHCP por endereço estático.

Use o console da VM para validar:

```bash
ip -4 -br address
```

```bash
ip route
```

Depois tente novamente o acesso pelo novo endereço.

### `hostname -f` não mostra `lab.test`

Confira:

```bash
hostnamectl
```

Depois:

```bash
cat /etc/hosts
```

Garanta que a entrada da própria VM contém o FQDN correto.

### Uma VM não resolve `servera` ou `serverb`

Confira:

```bash
getent hosts servera
```

Depois:

```bash
cat /etc/hosts
```

Verifique também:

```bash
cat /etc/resolv.conf
```

### SSH não responde

Confira:

```bash
systemctl status sshd --no-pager
```

```bash
sudo firewall-cmd --get-active-zones
```

```bash
sudo firewall-cmd --list-services
```

```bash
ss -lnt | grep ':22'
```

Não desabilite o firewall como solução.

### `dnf` não encontra pacotes

Confira:

```bash
sudo dnf repolist
```

Se estiver utilizando DVD:

```bash
mount | grep '/mnt/rhel-dvd'
```

Confira:

```bash
ls /mnt/rhel-dvd/BaseOS/repodata
ls /mnt/rhel-dvd/AppStream/repodata
```

Se estiver utilizando RHSM:

```bash
sudo subscription-manager identity
```

Não combine repositórios de versões diferentes do RHEL.

### SELinux não está Enforcing

Confira:

```bash
getenforce
```

```bash
sestatus
```

Não avance simplesmente colocando o sistema em modo permissivo.

### Os discos extras possuem partições ou sistemas de arquivos

Não utilize esses discos em outras tarefas antes dos laboratórios.

Confira:

```bash
lsblk -f
```

Se a topologia estiver diferente da documentação, investigue antes de criar o baseline.

---

## 4.23 Critério para avançar

Antes de continuar para a preparação do `bastion`, confirme:

```text
[ ] bastion.lab.test configurado
[ ] servera.lab.test configurado
[ ] serverb.lab.test configurado

[ ] bastion usa 192.168.100.10/24
[ ] servera usa 192.168.100.11/24
[ ] serverb usa 192.168.100.12/24

[ ] gateway 192.168.100.1 configurado nas três VMs
[ ] resolução bastion/servera/serverb funcionando

[ ] usuário student existe nas três VMs
[ ] student possui acesso administrativo via sudo

[ ] machine-id é diferente nas três VMs
[ ] SSH host keys são diferentes nas três VMs

[ ] sshd está ativo
[ ] firewalld está ativo
[ ] serviço SSH está autorizado no firewall
[ ] SELinux está Enforcing

[ ] existe uma fonte funcional de pacotes
[ ] python3 está instalado

[ ] discos adicionais de servera permanecem disponíveis
[ ] discos adicionais de serverb permanecem disponíveis

[ ] bastion alcança servera pela rede
[ ] bastion alcança serverb pela rede
```

A autenticação SSH por chave e a clonagem do projeto serão configuradas na etapa seguinte.

Continue para:

[05 — Preparação do bastion e clonagem](05-bastion-git.md)

[Índice](README.md) · [Home](../../README.md) · [Anterior](03-criacao-vms.md) · [Próximo](05-bastion-git.md)
