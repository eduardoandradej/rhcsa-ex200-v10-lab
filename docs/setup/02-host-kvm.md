# 02 — Preparação do host KVM/libvirt

[Índice](README.md) · [Home](../../README.md) · [Anterior](01-requisitos.md) · [Próximo](03-criacao-vms.md)

**Onde executar:** terminal do host KVM, com `sudo`.

## Validar virtualização e instalar ferramentas

```bash
lscpu
ls -l /dev/kvm
sudo dnf install -y qemu-kvm libvirt virt-install virt-viewer
sudo systemctl enable --now libvirtd
sudo virt-host-validate qemu
sudo virsh -c qemu:///system list --all
```

Se `/dev/kvm` não existir, confira o firmware e os módulos `kvm_intel`/`kvm_amd`. Em host que usa daemons modulares de libvirt, habilite os sockets correspondentes à instalação em vez de assumir `libvirtd`. Resolva falhas de KVM e permissões antes de criar as VMs; avisos de IOMMU não impedem este roteiro, que não usa passthrough.

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

Se já existir e estiver inativo, apenas inicie-o. Não redefina um pool existente. Este guia usa discos qcow2 nesse pool. Mantenha SELinux habilitado e use os diretórios padrão de libvirt.

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
