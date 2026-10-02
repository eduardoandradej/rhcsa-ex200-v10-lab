# 04 — Configuração inicial das VMs

[Índice](README.md) · [Home](../../README.md) · [Anterior](03-criacao-vms.md) · [Próximo](05-bastion-git.md)

**Onde executar:** console de cada VM, como `student` com `sudo`. Inicialmente, use o console se o SSH ainda não estiver acessível.

## Identidade e rede

Exemplo para **bastion**:

```bash
sudo hostnamectl set-hostname bastion.lab.example
nmcli connection show
```

Identifique o perfil ativo da interface ligada à rede `rhcsa-lab`. Substitua o valor abaixo pelo nome real; não suponha que a interface seja `eth0`:

```bash
LAB_CONNECTION='System eth0'
sudo nmcli connection modify "$LAB_CONNECTION" \
  ipv4.method manual ipv4.addresses 192.168.100.10/24 \
  ipv4.gateway 192.168.100.1 ipv4.dns 192.168.100.1 \
  ipv4.dns-search lab.example connection.autoconnect yes
sudo nmcli connection up "$LAB_CONNECTION"
```

Em **servera**, use hostname `servera.lab.example` e IP `192.168.100.11/24`. Em **serverb**, use `serverb.lab.example` e `192.168.100.12/24`. Gateway e DNS permanecem iguais. Reativar o perfil pode interromper a conexão SSH; faça pelo console.

Em cada VM, edite `sudoedit /etc/hosts` e adicione uma única vez:

```text
192.168.100.10 bastion.lab.example bastion
192.168.100.11 servera.lab.example servera
192.168.100.12 serverb.lab.example serverb
```

Não remova as entradas de localhost.

## Usuário, SSH e serviços

Se `student` não foi criado no instalador, crie-o em cada VM:

```bash
sudo useradd -m -G wheel student
sudo passwd student
```

Se já existir, apenas confira `id student` e o acesso com `sudo -v`.

```bash
sudo systemctl enable --now sshd
sudo systemctl enable --now firewalld
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload
getenforce
hostname -f
ip -4 address
ip route
lsblk -o NAME,SIZE,TYPE,MOUNTPOINTS
```

Preserve SELinux e firewall para praticar esses temas. Os discos extras não devem estar montados ou usados pelo sistema.

## Pacotes RHEL: escolher uma fonte

Use repositórios autorizados da sua instalação ou a ISO DVD local. Para repositório local, mantenha a ISO DVD conectada ao CD-ROM da VM; confira `lsblk` para identificar o dispositivo (normalmente `/dev/sr0`). Em cada VM:

```bash
sudo mkdir -p /mnt/rhel-dvd
sudo mount -o ro /dev/sr0 /mnt/rhel-dvd
ls /mnt/rhel-dvd/BaseOS/repodata /mnt/rhel-dvd/AppStream/repodata
```

Para persistência, adicione em `/etc/fstab` uma única entrada, após verificar o dispositivo:

```text
/dev/sr0 /mnt/rhel-dvd iso9660 ro,nofail 0 0
```

Crie `/etc/yum.repos.d/rhcsa-dvd.repo`:

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

Confira a chave indicada e use uma ISO da mesma versão do sistema. Não habilite simultaneamente fontes de versões diferentes. Repositório DVD não fornece atualizações posteriores à mídia.

```bash
sudo dnf repolist
sudo dnf install -y openssh-server openssh-clients python3 tar gzip bzip2 xz unzip zip
```

No bastion, `getent hosts servera serverb` e `ping -c 2 192.168.100.1` devem funcionar. Um ping não substitui a validação SSH da etapa seguinte.

**Antes de avançar:** IPs e nomes corretos, `student` em todas as VMs, SSH ativo e instalação de pacotes funcionando.

[Índice](README.md) · [Home](../../README.md) · [Anterior](03-criacao-vms.md) · [Próximo](05-bastion-git.md)
