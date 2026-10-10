# 02 — Preparação do host KVM/libvirt

[Índice](README.md) · [Home](../../README.md) · [Anterior](01-requisitos.md) · [Próximo](03-criacao-vms.md)

**Onde executar:** terminal do host KVM, com privilégios administrativos via `sudo`.

Esta etapa prepara o hospedeiro que executará as máquinas virtuais do laboratório. O objetivo é deixar KVM/QEMU, libvirt, armazenamento, rede virtual e ferramentas de administração prontos antes da criação de `bastion`, `servera` e `serverb`.

A preparação desta página é comum aos dois métodos de implantação:

- **Método A — instalação manual:** criação das VMs e instalação do RHEL a partir da mídia ISO;
- **Método B — imagem-base:** criação das VMs a partir de uma imagem QCOW2 previamente preparada.

---

## 2.1 Caminho principal — Ubuntu Desktop 24.04 LTS

Parta de um Ubuntu Desktop 24.04 LTS já instalado.

### 2.1.1 Instalar KVM, libvirt e ferramentas de administração

Atualize o índice de pacotes:

```bash
sudo apt update
```

Instale os componentes necessários:

```bash
sudo apt install -y \
  qemu-kvm \
  qemu-utils \
  libvirt-daemon-system \
  libvirt-clients \
  virtinst \
  virt-manager \
  virt-viewer \
  cpu-checker \
  libosinfo-bin \
  cockpit \
  cockpit-machines
```

Os principais componentes utilizados pelo projeto são:

| Componente | Finalidade |
|---|---|
| `qemu-kvm` | Virtualização acelerada por hardware |
| `qemu-utils` | Ferramentas para manipulação e validação de imagens, incluindo `qemu-img` |
| `libvirt-daemon-system` | Serviços de virtualização gerenciados pelo libvirt |
| `libvirt-clients` | Ferramentas de linha de comando, incluindo `virsh` |
| `virtinst` | Ferramentas de criação de VMs, incluindo `virt-install` |
| `virt-manager` | Administração gráfica das VMs |
| `virt-viewer` | Acesso gráfico ao console das VMs |
| `cpu-checker` | Validação de suporte à virtualização |
| `libosinfo-bin` | Informações de sistemas operacionais utilizadas pelo `virt-install` |
| `cockpit` | Administração web do hospedeiro |
| `cockpit-machines` | Gerenciamento de máquinas virtuais pelo Cockpit |

### 2.1.2 Habilitar os serviços

```bash
sudo systemctl enable --now libvirtd
sudo systemctl enable --now cockpit.socket
```

### 2.1.3 Adicionar o usuário aos grupos de virtualização

```bash
sudo usermod -aG kvm,libvirt "$USER"
```

Encerre a sessão do usuário e entre novamente para que a associação aos grupos seja atualizada.

O restante deste guia utiliza `sudo` nos comandos administrativos, portanto a atualização dos grupos não impede a continuidade da preparação.

### 2.1.4 Validar virtualização por hardware

Execute:

```bash
kvm-ok
```

Depois:

```bash
sudo virt-host-validate qemu
```

Confirme também o acesso ao libvirt:

```bash
sudo virsh -c qemu:///system list --all
```

Se a virtualização não estiver disponível, confirme no firmware da máquina se Intel VT-x ou AMD-V está habilitado.

Falhas reportadas por `virt-host-validate` devem ser investigadas antes da criação das VMs.

Referência oficial: [libvirt no Ubuntu](https://ubuntu.com/server/docs/how-to/virtualisation/libvirt/).

---

## 2.2 Caminho alternativo — RHEL 9 / Rocky Linux 9

Os comandos desta seção são destinados a hospedeiros da família RHEL.

Não execute os comandos `dnf` desta seção em um host Ubuntu.

### 2.2.1 Validar suporte à virtualização

Execute:

```bash
lscpu
```

Confirme também a presença do dispositivo KVM:

```bash
ls -l /dev/kvm
```

Se `/dev/kvm` não existir, verifique:

- se Intel VT-x ou AMD-V está habilitado no firmware;
- se o processador suporta virtualização;
- se `kvm_intel` ou `kvm_amd` está carregado.

Exemplos:

```bash
lsmod | grep '^kvm'
```

```bash
grep -Eo 'vmx|svm' /proc/cpuinfo | head
```

### 2.2.2 Instalar as ferramentas

```bash
sudo dnf install -y \
  qemu-kvm \
  libvirt \
  virt-install \
  virt-viewer \
  cockpit \
  cockpit-machines
```

O `virt-manager` é opcional quando o hospedeiro é administrado principalmente por Cockpit ou linha de comando.

Para instalá-lo:

```bash
sudo dnf install -y virt-manager
```

### 2.2.3 Habilitar os serviços do libvirt

Em instalações que utilizam os daemons modulares do libvirt, habilite os sockets necessários:

```bash
for drv in qemu network nodedev nwfilter secret storage interface; do
  sudo systemctl enable --now virt${drv}d{,-ro,-admin}.socket
done
```

Habilite também o Cockpit:

```bash
sudo systemctl enable --now cockpit.socket
```

> Dependendo da distribuição e da forma como o libvirt foi empacotado, `libvirtd` ainda pode estar disponível. O objetivo desta etapa é garantir que a conexão `qemu:///system` esteja funcional, independentemente do modelo de daemon utilizado pelo hospedeiro.

### 2.2.4 Validar o hospedeiro

Execute:

```bash
sudo virt-host-validate qemu
```

Depois:

```bash
sudo virsh -c qemu:///system list --all
```

Falhas (`FAIL`) devem ser investigadas antes da criação das VMs.

Avisos (`WARN`) devem ser avaliados conforme a funcionalidade envolvida. IOMMU, por exemplo, não é requisito deste laboratório, pois o projeto não utiliza passthrough de dispositivos.

---

## 2.3 Cockpit — administração e consultas rápidas

O Cockpit e o módulo `cockpit-machines` fazem parte da preparação do **host KVM**.

Não é necessário instalar o Cockpit nas três VMs apenas para administrar o hospedeiro e visualizar suas máquinas virtuais.

### 2.3.1 Confirmar o serviço

```bash
systemctl is-active cockpit.socket
```

Consulte detalhes:

```bash
systemctl status cockpit.socket --no-pager
```

### 2.3.2 Acessar a interface web

A interface web do Cockpit utiliza, por padrão, a porta TCP 9090.

No próprio hospedeiro:

```text
https://localhost:9090
```

A partir de outra estação da rede:

```text
https://ENDERECO_DO_HOST:9090
```

Entre com uma conta autorizada do **hospedeiro KVM**, e não com a conta `student` das VMs do laboratório.

Uma instalação com certificado local pode apresentar um aviso de certificado no primeiro acesso. Confirme que o endereço acessado corresponde ao seu hospedeiro antes de prosseguir.

O Cockpit pode ser utilizado para consultar:

- CPU e memória;
- serviços;
- logs;
- interfaces de rede;
- armazenamento;
- máquinas virtuais.

O módulo `cockpit-machines` adiciona a seção **Máquinas virtuais**.

Para ações administrativas, utilize a elevação de privilégios oferecida pela interface.

Para administração remota, a liberação da porta 9090 deve respeitar a política de firewall e segurança da rede em que o hospedeiro está instalado.

O roteiro não exige exposição do Cockpit à Internet.

Referências:

- [Cockpit — instalação](https://cockpit-project.org/running.html)
- [Cockpit — máquinas virtuais](https://cockpit-project.org/guide/latest/feature-virtualmachines.html)

### 2.3.3 Cockpit em Ubuntu via backports

No Ubuntu LTS, também é possível utilizar versões disponibilizadas pelos backports oficiais.

Com `noble-backports` habilitado:

```bash
sudo apt install -t noble-backports cockpit cockpit-machines
```

Essa é uma opção de atualização.

A instalação inicial descrita anteriormente utiliza os repositórios já habilitados no sistema.

---

## 2.4 Etapas comuns aos hospedeiros

A partir deste ponto, o procedimento é o mesmo independentemente de o hospedeiro utilizar Ubuntu, RHEL ou Rocky Linux.

Antes de criar recursos, inspecione o ambiente existente:

```bash
ip route
```

```bash
sudo virsh -c qemu:///system net-list --all
```

```bash
sudo virsh -c qemu:///system pool-list --all
```

O projeto utiliza como padrão:

| Recurso | Valor |
|---|---|
| Rede libvirt | `rhcsa-lab` |
| Bridge virtual | `virbr-rhcsa` |
| Rede IPv4 | `192.168.100.0/24` |
| Gateway | `192.168.100.1` |
| Domínio | `lab.test` |
| Pool principal | `default` |
| Diretório dos discos | `/var/lib/libvirt/images` |

Antes de criar a rede, confirme que `192.168.100.0/24` não conflita com:

- rede local;
- VPN;
- outra bridge;
- outra rede libvirt;
- redes utilizadas por containers.

---

## 2.5 Preparar o armazenamento

Liste os pools existentes:

```bash
sudo virsh -c qemu:///system pool-list --all
```

### 2.5.1 Se o pool `default` já existir

Se estiver ativo, não faça alterações.

Se estiver inativo:

```bash
sudo virsh -c qemu:///system pool-start default
```

Para habilitar inicialização automática:

```bash
sudo virsh -c qemu:///system pool-autostart default
```

### 2.5.2 Se o pool `default` não existir

Crie o diretório:

```bash
sudo mkdir -p /var/lib/libvirt/images
```

Defina o pool:

```bash
sudo virsh -c qemu:///system \
  pool-define-as default dir \
  --target /var/lib/libvirt/images
```

Inicie:

```bash
sudo virsh -c qemu:///system pool-start default
```

Habilite autostart:

```bash
sudo virsh -c qemu:///system pool-autostart default
```

Valide:

```bash
sudo virsh -c qemu:///system pool-info default
```

Este projeto utiliza discos QCOW2 armazenados nesse pool.

Em hospedeiros RHEL/Rocky, mantenha SELinux habilitado.

Em Ubuntu, preserve as proteções AppArmor utilizadas pelo libvirt.

Não desabilite mecanismos de segurança para fazer o laboratório funcionar.

---

## 2.6 Criar a rede NAT do laboratório

Antes de criar a rede, confira novamente as rotas:

```bash
ip route
```

Confira as redes do libvirt:

```bash
sudo virsh -c qemu:///system net-list --all
```

A rede padrão deste projeto será:

```text
Nome:       rhcsa-lab
Bridge:     virbr-rhcsa
Rede:       192.168.100.0/24
Gateway:    192.168.100.1
Domínio:    lab.test
DHCP:       192.168.100.100 a 192.168.100.199
```

Os endereços fixos das VMs ficam fora da faixa DHCP:

```text
bastion   192.168.100.10
servera   192.168.100.11
serverb   192.168.100.12
```

### 2.6.1 Criar o XML da rede

Crie `/tmp/rhcsa-lab.xml`:

```bash
cat > /tmp/rhcsa-lab.xml <<'XML'
<network>
  <name>rhcsa-lab</name>
  <forward mode='nat'/>
  <bridge name='virbr-rhcsa' stp='on' delay='0'/>
  <domain name='lab.test'/>
  <ip address='192.168.100.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='192.168.100.100' end='192.168.100.199'/>
    </dhcp>
  </ip>
</network>
XML
```

Defina a rede:

```bash
sudo virsh -c qemu:///system net-define /tmp/rhcsa-lab.xml
```

Inicie:

```bash
sudo virsh -c qemu:///system net-start rhcsa-lab
```

Habilite autostart:

```bash
sudo virsh -c qemu:///system net-autostart rhcsa-lab
```

### 2.6.2 Validar a rede

Consulte:

```bash
sudo virsh -c qemu:///system net-info rhcsa-lab
```

Confira o XML efetivamente aplicado:

```bash
sudo virsh -c qemu:///system net-dumpxml rhcsa-lab
```

Valide a bridge:

```bash
ip addr show virbr-rhcsa
```

Ela deve possuir:

```text
192.168.100.1/24
```

### 2.6.3 Se a rede já existir

Não redefina automaticamente uma rede existente.

Primeiro consulte:

```bash
sudo virsh -c qemu:///system net-dumpxml rhcsa-lab
```

Reutilize-a somente se corresponder ao plano de endereçamento deste projeto.

---

## 2.7 Preparar a origem das VMs

A origem necessária depende do método escolhido na etapa seguinte.

### 2.7.1 Método A — instalação manual

O Método A utiliza a mídia ISO oficial do RHEL.

Se desejar seguir esse método, disponibilize a ISO no hospedeiro.

O roteiro utiliza como referência:

```text
/var/lib/libvirt/images/rhel-9.8-x86_64-dvd.iso
```

Esse caminho é apenas uma convenção do projeto e pode ser adaptado.

Confira:

```bash
ls -lh /var/lib/libvirt/images/rhel-9.8-x86_64-dvd.iso
```

Valide a integridade da ISO utilizando o checksum fornecido pela origem oficial.

A mídia ISO não é distribuída por este repositório.

### 2.7.2 Método B — imagem-base

O Método B não exige a ISO para criar `bastion`, `servera` e `serverb`.

A imagem QCOW2 e seu checksum serão preparados e validados na página:

[3.2 — Método B: implantação a partir da imagem-base](03b-imagem-template.md)

Não copie a imagem para o pool nem crie as VMs nesta etapa.

A página do Método B executa esse procedimento de forma controlada.

---

## 2.8 Validação final do host

Antes de prosseguir, faça uma última conferência.

### 2.8.1 Libvirt

```bash
sudo virsh -c qemu:///system list --all
```

### 2.8.2 Pool

```bash
sudo virsh -c qemu:///system pool-info default
```

O pool deve aparecer como ativo.

### 2.8.3 Rede

```bash
sudo virsh -c qemu:///system net-info rhcsa-lab
```

A rede deve estar:

```text
Active: yes
Autostart: yes
```

### 2.8.4 Bridge

```bash
ip -br addr show virbr-rhcsa
```

A bridge deve possuir o endereço:

```text
192.168.100.1/24
```

### 2.8.5 Ferramentas

Confirme:

```bash
command -v virsh
command -v virt-install
command -v qemu-img
```

Se utilizar interface gráfica:

```bash
command -v virt-viewer
```

---

## 2.9 Critério para avançar

Antes de prosseguir para a criação das máquinas virtuais, confirme:

```text
[ ] virtualização por hardware validada
[ ] acesso qemu:///system funcionando
[ ] KVM/QEMU instalado
[ ] libvirt operacional
[ ] virt-install disponível
[ ] qemu-img disponível

[ ] pool default ativo
[ ] diretório /var/lib/libvirt/images disponível

[ ] rede rhcsa-lab ativa
[ ] bridge virbr-rhcsa criada
[ ] gateway 192.168.100.1 configurado
[ ] faixa 192.168.100.0/24 sem conflito

[ ] Cockpit funcional, se escolhido para administração

[ ] Método A ou Método B definido
```

Se utilizar o **Método A**:

```text
[ ] ISO oficial do RHEL disponível
[ ] integridade da ISO validada
```

Se utilizar o **Método B**:

```text
[ ] host preparado para receber e validar a imagem-base
```

Com o hospedeiro preparado, prossiga para:

[03 — Criação das máquinas virtuais](03-criacao-vms.md)

[Índice](README.md) · [Home](../../README.md) · [Anterior](01-requisitos.md) · [Próximo](03-criacao-vms.md)
