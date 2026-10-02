# 03 — Criação das máquinas virtuais

[Índice](README.md) · [Home](../../README.md) · [Anterior](02-host-kvm.md) · [Próximo](04-configuracao-vms.md)

**Onde executar:** host KVM. Esta etapa cria VMs novas; não execute os comandos sobre nomes/discos já usados.

## Criar bastion, servera e serverb

```bash
sudo virsh -c qemu:///system list --all
```

Abra uma sessão gráfica no host para acompanhar o instalador. Se o host for remoto, use virt-manager por uma conexão libvirt/SSH autorizada. Os comandos usam `--noautoconsole`; conecte ao console gráfico para instalar o sistema.

```bash
sudo virt-install --connect qemu:///system --name bastion \
  --memory 2048 --vcpus 2 --cpu host --osinfo detect=on,require=off \
  --disk pool=default,size=30,format=qcow2,bus=virtio \
  --network network=rhcsa-lab,model=virtio \
  --cdrom /var/lib/libvirt/images/rhel-9.8-x86_64-dvd.iso \
  --graphics vnc,listen=127.0.0.1 --noautoconsole

sudo virt-install --connect qemu:///system --name servera \
  --memory 3072 --vcpus 2 --cpu host --osinfo detect=on,require=off \
  --disk pool=default,size=30,format=qcow2,bus=virtio \
  --disk pool=default,size=5,format=qcow2,bus=virtio \
  --disk pool=default,size=5,format=qcow2,bus=virtio \
  --disk pool=default,size=3,format=qcow2,bus=virtio \
  --disk pool=default,size=2,format=qcow2,bus=virtio \
  --network network=rhcsa-lab,model=virtio \
  --cdrom /var/lib/libvirt/images/rhel-9.8-x86_64-dvd.iso \
  --graphics vnc,listen=127.0.0.1 --noautoconsole

sudo virt-install --connect qemu:///system --name serverb \
  --memory 2048 --vcpus 2 --cpu host --osinfo detect=on,require=off \
  --disk pool=default,size=30,format=qcow2,bus=virtio \
  --disk pool=default,size=5,format=qcow2,bus=virtio \
  --disk pool=default,size=3,format=qcow2,bus=virtio \
  --network network=rhcsa-lab,model=virtio \
  --cdrom /var/lib/libvirt/images/rhel-9.8-x86_64-dvd.iso \
  --graphics vnc,listen=127.0.0.1 --noautoconsole
```

Abra cada console (ou selecione a VM no virt-manager):

```bash
sudo virt-viewer --connect qemu:///system bastion
sudo virt-viewer --connect qemu:///system servera
sudo virt-viewer --connect qemu:///system serverb
```

## Instalar o sistema nas três VMs

1. Instale RHEL 9.8; escolha instalação mínima.
2. No destino da instalação, selecione **somente o disco de 30 GiB (`vda`)**. Deixe os discos extras sem partições para os exercícios.
3. Configure hostname e IP conforme a etapa 4, durante o instalador ou após instalar.
4. Crie `student` como administrador e defina senhas locais. Não publique as senhas.
5. Conclua a instalação e reinicie pelo disco do sistema.

Depois, no host, verifique discos e interfaces:

```bash
sudo virsh -c qemu:///system domblklist servera
sudo virsh -c qemu:///system domblklist serverb
sudo virsh -c qemu:///system domiflist bastion
```

**Antes de avançar:** três VMs instaladas, inicializando pelo disco, com discos extras preservados. Valide tamanhos e nomes com `lsblk` dentro de cada VM.

[Índice](README.md) · [Home](../../README.md) · [Anterior](02-host-kvm.md) · [Próximo](04-configuracao-vms.md)
