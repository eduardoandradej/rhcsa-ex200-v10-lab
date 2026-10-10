# 3.1 — Método A: instalação manual a partir da ISO do RHEL

[Criação das VMs](03-criacao-vms.md) · [Índice](README.md) · [Home](../../README.md) · [Anterior](02-host-kvm.md) · [Próximo](04-configuracao-vms.md)

Este método cria as três máquinas virtuais do laboratório individualmente e instala o Red Hat Enterprise Linux a partir da mídia ISO.

É o método recomendado para quem deseja praticar também a criação das VMs, a instalação do sistema operacional e a identificação dos discos utilizados pelo laboratório.

## 3.1.1 Resultado esperado

Ao final desta etapa, o host KVM deverá possuir:

| VM | RAM | vCPU | Disco do sistema | Discos adicionais |
|---|---:|---:|---:|---|
| `bastion` | 2 GiB | 2 | 30 GiB | nenhum |
| `servera` | 3 GiB | 2 | 30 GiB | 5 GiB, 5 GiB, 3 GiB e 2 GiB |
| `serverb` | 2 GiB | 2 | 30 GiB | 5 GiB e 3 GiB |

Os discos adicionais não devem ser particionados durante a instalação do RHEL. Eles serão utilizados posteriormente pelos exercícios de armazenamento.

---

## 3.1.2 Onde executar

**Local:** host KVM/libvirt.

Os comandos desta página devem ser executados no sistema que hospeda as máquinas virtuais, e não dentro de `bastion`, `servera` ou `serverb`.

Confirme o host antes de continuar:

```bash
hostnamectl
```

---

## 3.1.3 Pré-requisitos

Antes de criar as máquinas, confirme que:

- KVM/libvirt está instalado e operacional;
- o serviço libvirt está ativo;
- a rede `rhcsa-lab` foi criada na etapa anterior;
- o pool de armazenamento `default` está disponível;
- a ISO do RHEL está armazenada no host;
- não existem VMs antigas utilizando os nomes `bastion`, `servera` ou `serverb`.

Confirme o libvirt:

```bash
sudo virsh -c qemu:///system list --all
```

Confirme as redes:

```bash
sudo virsh -c qemu:///system net-list --all
```

A rede do laboratório deverá aparecer como ativa:

```text
Name        State    Autostart   Persistent
------------------------------------------------
rhcsa-lab   active   yes         yes
```

Confirme o pool de armazenamento:

```bash
sudo virsh -c qemu:///system pool-list --all
```

Confirme a presença da ISO:

```bash
ls -lh /var/lib/libvirt/images/rhel-9.8-x86_64-dvd.iso
```

> O nome e o caminho da ISO podem ser diferentes no seu host. Se necessário, ajuste o parâmetro `--cdrom` nos comandos desta página.

---

## 3.1.4 Verificar se os nomes das VMs estão disponíveis

Execute:

```bash
sudo virsh -c qemu:///system list --all
```

Não prossiga se já existirem domínios chamados:

```text
bastion
servera
serverb
```

Esta documentação considera uma instalação nova.

---

## 3.1.5 Criar a VM bastion

A VM `bastion` será a estação de controle do laboratório.

Ela hospedará posteriormente o repositório Git, Ansible e o comando `lab`.

Execute:

```bash
sudo virt-install \
  --connect qemu:///system \
  --name bastion \
  --memory 2048 \
  --vcpus 2 \
  --cpu host \
  --osinfo detect=on,require=off \
  --disk pool=default,size=30,format=qcow2,bus=virtio \
  --network network=rhcsa-lab,model=virtio \
  --cdrom /var/lib/libvirt/images/rhel-9.8-x86_64-dvd.iso \
  --graphics vnc,listen=127.0.0.1 \
  --noautoconsole
```

Confirme a criação:

```bash
sudo virsh -c qemu:///system list --all
```

Verifique o disco associado:

```bash
sudo virsh -c qemu:///system domblklist bastion
```

A VM deve possuir um disco principal de 30 GiB.

---

## 3.1.6 Criar a VM servera

`servera` é o principal alvo dos exercícios RHCSA.

Além do disco do sistema, ela recebe quatro discos adicionais para os laboratórios de particionamento, LVM, sistemas de arquivos e swap.

Execute:

```bash
sudo virt-install \
  --connect qemu:///system \
  --name servera \
  --memory 3072 \
  --vcpus 2 \
  --cpu host \
  --osinfo detect=on,require=off \
  --disk pool=default,size=30,format=qcow2,bus=virtio \
  --disk pool=default,size=5,format=qcow2,bus=virtio \
  --disk pool=default,size=5,format=qcow2,bus=virtio \
  --disk pool=default,size=3,format=qcow2,bus=virtio \
  --disk pool=default,size=2,format=qcow2,bus=virtio \
  --network network=rhcsa-lab,model=virtio \
  --cdrom /var/lib/libvirt/images/rhel-9.8-x86_64-dvd.iso \
  --graphics vnc,listen=127.0.0.1 \
  --noautoconsole
```

Confira:

```bash
sudo virsh -c qemu:///system domblklist servera
```

Depois da instalação, a expectativa é que o RHEL reconheça os discos VirtIO aproximadamente como:

```text
/dev/vda   30 GiB   disco do sistema
/dev/vdb    5 GiB   laboratório
/dev/vdc    5 GiB   laboratório
/dev/vdd    3 GiB   laboratório
/dev/vde    2 GiB   laboratório
```

A ordem deve ser validada dentro da VM com `lsblk`.

---

## 3.1.7 Criar a VM serverb

`serverb` funciona como segundo host do laboratório e fornece recursos utilizados por exercícios que envolvem comunicação entre sistemas.

Execute:

```bash
sudo virt-install \
  --connect qemu:///system \
  --name serverb \
  --memory 2048 \
  --vcpus 2 \
  --cpu host \
  --osinfo detect=on,require=off \
  --disk pool=default,size=30,format=qcow2,bus=virtio \
  --disk pool=default,size=5,format=qcow2,bus=virtio \
  --disk pool=default,size=3,format=qcow2,bus=virtio \
  --network network=rhcsa-lab,model=virtio \
  --cdrom /var/lib/libvirt/images/rhel-9.8-x86_64-dvd.iso \
  --graphics vnc,listen=127.0.0.1 \
  --noautoconsole
```

Confira:

```bash
sudo virsh -c qemu:///system domblklist serverb
```

Depois da instalação, a expectativa é:

```text
/dev/vda   30 GiB   disco do sistema
/dev/vdb    5 GiB   laboratório
/dev/vdc    3 GiB   laboratório
```

---

## 3.1.8 Confirmar as três VMs

Execute:

```bash
sudo virsh -c qemu:///system list --all
```

As três máquinas devem aparecer:

```text
bastion
servera
serverb
```

Consulte também as interfaces virtuais:

```bash
sudo virsh -c qemu:///system domiflist bastion
sudo virsh -c qemu:///system domiflist servera
sudo virsh -c qemu:///system domiflist serverb
```

Cada VM deve possuir sua própria interface e endereço MAC.

---

## 3.1.9 Abrir o console de instalação

Os comandos `virt-install` utilizam:

```text
--graphics vnc,listen=127.0.0.1
--noautoconsole
```

Isso significa que a VM é criada sem prender o terminal ao instalador.

Em um host com ambiente gráfico, uma opção é utilizar:

```bash
virt-manager
```

Também é possível utilizar `virt-viewer`:

```bash
sudo virt-viewer --connect qemu:///system bastion
```

Para as demais:

```bash
sudo virt-viewer --connect qemu:///system servera
sudo virt-viewer --connect qemu:///system serverb
```

Se o host KVM for administrado remotamente, utilize uma forma de acesso gráfico compatível com sua infraestrutura.

---

## 3.1.10 Instalar o RHEL no bastion

No instalador do RHEL, configure o sistema normalmente.

Para o disco de instalação, utilize somente o disco de **30 GiB**.

No `bastion` não existem discos adicionais, portanto a seleção é direta.

Defina o hostname:

```text
bastion.lab.test
```

Crie o usuário:

```text
student
```

A senha local utilizada no seu laboratório não deve ser publicada no repositório Git.

Conclua a instalação e reinicie a VM.

---

## 3.1.11 Instalar o RHEL no servera

Este ponto exige mais atenção.

`servera` possui cinco discos:

```text
30 GiB
5 GiB
5 GiB
3 GiB
2 GiB
```

No instalador, selecione **somente o disco de 30 GiB** como destino da instalação.

Não crie partições, LVM ou sistemas de arquivos nos quatro discos adicionais.

Eles devem permanecer intactos para os exercícios.

Defina o hostname:

```text
servera.lab.test
```

Crie também o usuário:

```text
student
```

Conclua a instalação e reinicie a VM.

---

## 3.1.12 Instalar o RHEL no serverb

`serverb` possui:

```text
30 GiB
5 GiB
3 GiB
```

Novamente, utilize **somente o disco de 30 GiB** para instalar o sistema operacional.

Os discos de 5 GiB e 3 GiB devem permanecer sem uso.

Defina:

```text
serverb.lab.test
```

Crie o usuário:

```text
student
```

Conclua a instalação e reinicie.

---

## 3.1.13 Confirmar que as VMs inicializam pelo disco

Depois da instalação, confirme:

```bash
sudo virsh -c qemu:///system list --all
```

Se necessário, inicie uma VM manualmente:

```bash
sudo virsh -c qemu:///system start bastion
sudo virsh -c qemu:///system start servera
sudo virsh -c qemu:///system start serverb
```

As máquinas devem inicializar normalmente pelo sistema instalado.

---

## 3.1.14 Validar os discos dentro das VMs

Entre em cada VM pelo console e execute:

```bash
lsblk
```

No `bastion`, deve existir apenas o disco de sistema:

```text
vda    30G
```

No `servera`, devem aparecer:

```text
vda    30G
vdb     5G
vdc     5G
vdd     3G
vde     2G
```

No `serverb`:

```text
vda    30G
vdb     5G
vdc     3G
```

O ponto mais importante é confirmar que os discos adicionais não possuem partições ou sistemas de arquivos criados durante a instalação.

Uma verificação mais detalhada pode ser feita com:

```bash
lsblk -f
```

---

## 3.1.15 Validar os discos pelo host KVM

No host:

```bash
sudo virsh -c qemu:///system domblklist bastion
```

Depois:

```bash
sudo virsh -c qemu:///system domblklist servera
```

E:

```bash
sudo virsh -c qemu:///system domblklist serverb
```

Isso permite conferir quais arquivos de disco estão associados a cada domínio.

---

## 3.1.16 Validar as interfaces de rede

No host KVM:

```bash
sudo virsh -c qemu:///system domiflist bastion
sudo virsh -c qemu:///system domiflist servera
sudo virsh -c qemu:///system domiflist serverb
```

Confirme que todas as interfaces estão associadas à rede:

```text
rhcsa-lab
```

Cada VM deve possuir um endereço MAC diferente.

---

## 3.1.17 Problemas comuns

### A VM já existe

Exemplo:

```text
ERROR: Domain name 'servera' already exists
```

Confirme:

```bash
sudo virsh -c qemu:///system list --all
```

Não sobrescreva uma VM existente sem saber se ela contém dados que precisam ser preservados.

### A ISO não foi encontrada

Confirme o caminho:

```bash
ls -lh /var/lib/libvirt/images/
```

Ajuste `--cdrom` para o caminho real da mídia.

### A rede `rhcsa-lab` não existe

Confira:

```bash
sudo virsh -c qemu:///system net-list --all
```

Se ela não existir, retorne à etapa:

[02 — Preparação do host KVM/libvirt](02-host-kvm.md)

### A VM não inicializa

Consulte:

```bash
sudo virsh -c qemu:///system list --all
```

Tente iniciar:

```bash
sudo virsh -c qemu:///system start NOME_DA_VM
```

Consulte detalhes:

```bash
sudo virsh -c qemu:///system dominfo NOME_DA_VM
```

### O servera não possui todos os discos

Confira no host:

```bash
sudo virsh -c qemu:///system domblklist servera
```

E dentro da VM:

```bash
lsblk
```

Não avance para os laboratórios de armazenamento enquanto a topologia de discos não estiver correta.

---

## 3.1.18 Critério para concluir o Método A

Antes de avançar, confirme:

```text
[ ] bastion existe no libvirt
[ ] servera existe no libvirt
[ ] serverb existe no libvirt

[ ] as três VMs inicializam pelo disco do sistema
[ ] o RHEL está instalado nas três VMs
[ ] o usuário student existe nas três VMs

[ ] bastion possui disco de sistema de 30 GiB

[ ] servera possui:
    30 GiB
     5 GiB
     5 GiB
     3 GiB
     2 GiB

[ ] serverb possui:
    30 GiB
     5 GiB
     3 GiB

[ ] somente o disco de sistema foi utilizado durante a instalação
[ ] os discos adicionais permanecem disponíveis para os laboratórios
[ ] cada VM possui sua própria interface de rede
```

Se todos os itens estiverem corretos, o Método A está concluído.

Continue para:

[04 — Configuração inicial das VMs](04-configuracao-vms.md)

[Criação das VMs](03-criacao-vms.md) · [Índice](README.md) · [Home](../../README.md) · [Anterior](02-host-kvm.md) · [Próximo](04-configuracao-vms.md)S