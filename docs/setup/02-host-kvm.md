# 02 — Preparação do host KVM/libvirt

[Índice](README.md) · [Home](../../README.md) · [Anterior](01-requisitos.md) · [Próximo](03-criacao-vms.md)

**Onde executar:** terminal do host KVM, com `sudo`.

## Caminho principal — Ubuntu Desktop 24.04 LTS

Parta de um Ubuntu Desktop instalado. Instale no hospedeiro:

```bash
sudo apt update
sudo apt install -y qemu-kvm libvirt-daemon-system libvirt-clients \
  virtinst virt-manager virt-viewer cpu-checker libosinfo-bin cockpit cockpit-machines
sudo systemctl enable --now libvirtd
sudo systemctl enable --now cockpit.socket
sudo usermod -aG kvm,libvirt "$USER"
kvm-ok
sudo virt-host-validate qemu
sudo virsh -c qemu:///system list --all
```

Encerre a sessão e entre novamente para atualizar os grupos. O virt-manager e o navegador são usados diretamente na sessão Desktop do hospedeiro. O restante do guia pode usar `sudo virsh` independentemente da atualização dos grupos.

Referência oficial: [libvirt no Ubuntu](https://ubuntu.com/server/docs/how-to/virtualisation/libvirt/).

## Caminho alternativo — Rocky Linux 9.8 / RHEL 9

Os comandos seguintes são a alternativa para host Rocky/RHEL; não execute `dnf` no Ubuntu.

### Validar virtualização e instalar ferramentas

```bash
lscpu
ls -l /dev/kvm
sudo dnf install -y qemu-kvm libvirt virt-install virt-manager virt-viewer cockpit cockpit-machines
sudo systemctl enable --now libvirtd
sudo systemctl enable --now cockpit.socket
sudo virt-host-validate qemu
sudo virsh -c qemu:///system list --all
```

Se `/dev/kvm` não existir, confira o firmware e os módulos `kvm_intel`/`kvm_amd`. Em host que usa daemons modulares de libvirt, habilite os sockets correspondentes à instalação em vez de assumir `libvirtd`. Resolva falhas de KVM e permissões antes de criar as VMs; avisos de IOMMU não impedem este roteiro, que não usa passthrough.

## Cockpit — consultas rápidas no hospedeiro

O Cockpit e `cockpit-machines` fazem parte da preparação do **host** nos dois caminhos acima. Não é necessário instalá-los nas três VMs para consultar o hospedeiro e suas máquinas virtuais.

Confira o serviço:

```bash
systemctl is-active cockpit.socket
systemctl status cockpit.socket --no-pager
```

No navegador do próprio Desktop, abra **[https://localhost:9090](https://localhost:9090)**. Entre com o usuário e a senha do hospedeiro (por exemplo, `eduardo`), não com a conta `student` do bastion. Uma instalação com certificado local pode mostrar um aviso no navegador; confira que o endereço é o seu host antes de continuar.

Use o painel para consultar CPU e memória, serviços, logs, interfaces e a seção **Máquinas virtuais**. Algumas páginas dependem dos módulos instalados e da configuração do sistema. Para ações administrativas, use a elevação de privilégios oferecida pela interface.

O acesso local basta para este roteiro. Não é necessário abrir a porta 9090 no firewall para acessar pelo navegador do próprio host.

Referências: [instalação oficial do Cockpit](https://cockpit-project.org/running.html) e [módulo de máquinas virtuais](https://cockpit-project.org/guide/latest/feature-virtualmachines.html).

No Ubuntu LTS, o projeto Cockpit também recomenda versões dos backports oficiais. Para optar por esse canal, com `noble-backports` habilitado, instale os dois pacotes do mesmo canal:

```bash
sudo apt install -t noble-backports cockpit cockpit-machines
```

Esse comando é uma opção de atualização; a instalação inicial acima usa os repositórios Ubuntu habilitados. Confirme os pacotes disponíveis antes de alterar o canal.

## Etapas comuns aos dois hospedeiros

Antes de criar rede ou pool, inspecione o ambiente existente. O histórico do script original usa a rede `rhel-lab`, bridge `virbr100` e ISOs em `/var/lib/libvirt/iso`. Os nomes `rhcsa-lab` e `virbr-rhcsa` abaixo são os nomes do roteiro público de instalação nova. Ambos podem representar a mesma arquitetura, mas não crie duas redes com a mesma faixa. Se sua rede `rhel-lab` já existir, confira seu XML e use esse nome nos comandos `--network` da etapa 3. O caminho da ISO também pode ser adaptado à instalação existente.

```bash
sudo virsh -c qemu:///system net-list --all
sudo virsh -c qemu:///system pool-list --all
```

## Armazenamento

```bash
sudo virsh -c qemu:///system pool-list --all
```

Se o pool `default` não existir:

```bash
sudo mkdir -p /var/lib/libvirt/images
sudo virsh -c qemu:///system pool-define-as default dir --target /var/lib/libvirt/images
sudo virsh -c qemu:///system pool-start default
sudo virsh -c qemu:///system pool-autostart default
```

Se já existir e estiver inativo, apenas inicie-o. Não redefina um pool existente. Este guia usa discos qcow2 nesse pool. Use os diretórios padrão de libvirt. No Rocky/RHEL, mantenha SELinux habilitado; no Ubuntu, preserve as proteções AppArmor de libvirt. Não é necessário desabilitar esses mecanismos para seguir o roteiro.

## Rede NAT

Inspecione redes e rotas existentes antes de aplicar:

```bash
ip route
sudo virsh -c qemu:///system net-list --all
```

Crie `/tmp/rhcsa-lab.xml`:

```bash
cat > /tmp/rhcsa-lab.xml <<'XML'
<network>
  <name>rhcsa-lab</name>
  <forward mode='nat'/>
  <bridge name='virbr-rhcsa' stp='on' delay='0'/>
  <domain name='lab.example'/>
  <ip address='192.168.100.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='192.168.100.100' end='192.168.100.199'/>
    </dhcp>
  </ip>
</network>
XML
sudo virsh -c qemu:///system net-define /tmp/rhcsa-lab.xml
sudo virsh -c qemu:///system net-start rhcsa-lab
sudo virsh -c qemu:///system net-autostart rhcsa-lab
sudo virsh -c qemu:///system net-info rhcsa-lab
```

Se a rede já existir, confira `net-dumpxml rhcsa-lab` e reutilize apenas se corresponder ao plano. Os IPs fixos das VMs ficam fora da faixa DHCP.

Copie a ISO DVD autorizada para `/var/lib/libvirt/images/rhel-9.8-x86_64-dvd.iso`. Esse nome é o caminho local adotado pelo guia, não uma URL de download. Confira integridade com o checksum fornecido pela origem da ISO.

**Antes de avançar:** KVM validado, pool ativo, rede ativa e ISO acessível.

[Índice](README.md) · [Home](../../README.md) · [Anterior](01-requisitos.md) · [Próximo](03-criacao-vms.md)
