# 3.2 — Método B: implantação a partir da imagem-base

[Criação das VMs](03-criacao-vms.md) · [Índice](README.md) · [Home](../../README.md) · [Anterior](03a-instalacao-manual.md) · [Próximo](04-configuracao-vms.md)

Este método cria o ambiente do laboratório a partir de uma imagem-base QCOW2 previamente preparada.

O objetivo é reduzir o tempo necessário para reconstruir o ambiente, mantendo as três máquinas virtuais independentes e preservando a arquitetura utilizada pelos laboratórios.

O uso da imagem-base não elimina as etapas de individualização das VMs. Cada máquina deverá possuir disco próprio, endereço MAC próprio, identidade de máquina própria e chaves SSH próprias.

## 3.2.1 Resultado esperado

Ao final deste método, o host KVM deverá possuir:

| VM | RAM | vCPU | Disco do sistema | Discos adicionais |
|---|---:|---:|---:|---|
| `bastion` | 2 GiB | 2 | 30 GiB | nenhum |
| `servera` | 3 GiB | 2 | 30 GiB | 5 GiB, 5 GiB, 3 GiB e 2 GiB |
| `serverb` | 2 GiB | 2 | 30 GiB | 5 GiB e 3 GiB |

A arquitetura final será:

```text
                         Host KVM/libvirt
                                |
                         rede rhcsa-lab
                         192.168.100.0/24
                                |
              +-----------------+-----------------+
              |                 |                 |
           bastion            servera           serverb
       192.168.100.10     192.168.100.11    192.168.100.12
              |                 |                 |
           30 GiB            30 GiB            30 GiB
                                |                 |
                           +----+----+          +-+-+
                           | | | |             |   |
                           5 5 3 2 GiB          5   3 GiB
```

Os endereços IP definitivos e os hostnames serão configurados na etapa 04.

---

## 3.2.2 Onde executar

**Local:** host KVM/libvirt.

Os comandos desta página devem ser executados no hospedeiro das máquinas virtuais.

Não execute os comandos de manipulação de discos QCOW2 dentro de `bastion`, `servera` ou `serverb`.

Confirme o host:

```bash
hostnamectl
```

Confirme o libvirt:

```bash
sudo virsh -c qemu:///system list --all
```

---

## 3.2.3 Pré-requisitos

Antes de utilizar a imagem-base, confirme que a etapa de preparação do host foi concluída.

Devem estar disponíveis:

```text
KVM/QEMU
libvirt
virt-install
qemu-img
rede rhcsa-lab
pool de armazenamento default
```

Confirme a rede:

```bash
sudo virsh -c qemu:///system net-list --all
```

Resultado esperado:

```text
Name        State    Autostart   Persistent
------------------------------------------------
rhcsa-lab   active   yes         yes
```

Confirme o pool:

```bash
sudo virsh -c qemu:///system pool-list --all
```

O pool `default` deve estar ativo.

Confira também se os nomes das VMs estão disponíveis:

```bash
sudo virsh -c qemu:///system list --all
```

Não prossiga se já existirem máquinas chamadas:

```text
bastion
servera
serverb
```

Este procedimento considera uma implantação nova.

---

## 3.2.4 Sobre a imagem-base

A imagem utilizada neste método é:

```text
rhel-rhcsa-base-v1.qcow2
```

Ela possui um sistema RHEL previamente instalado e preparado para servir como origem para novas VMs.

O arquivo original deve ser tratado como **somente leitura**.

Nunca utilize a imagem-base diretamente como disco de uma VM de laboratório.

O fluxo correto é:

```text
rhel-rhcsa-base-v1.qcow2
          |
          +---- cópia independente ----> bastion.qcow2
          |
          +---- cópia independente ----> servera.qcow2
          |
          +---- cópia independente ----> serverb.qcow2
```

As três VMs serão, portanto, independentes da imagem original.

---

## 3.2.5 Download da imagem

A distribuição pública da imagem-base deve observar os termos aplicáveis ao Red Hat Enterprise Linux.

A imagem-base e o arquivo de verificação SHA-256 estão disponíveis na pasta pública do projeto no Google Drive:

[Baixar imagem-base do laboratório](https://drive.google.com/drive/folders/1j7k401rD8cCLUWR0aHalU-KVS-MwG8G4?usp=sharing0)

```text
rhel-rhcsa-base-v1.qcow2
rhel-rhcsa-base-v1.qcow2.sha256
```

Localize os dois arquivos no host KVM.

Exemplo:

```bash
cd ~/Downloads
ls -lh rhel-rhcsa-base-v1.qcow2*
```

Resultado esperado:

```text
rhel-rhcsa-base-v1.qcow2
rhel-rhcsa-base-v1.qcow2.sha256
```

> Não prossiga antes de validar a integridade da imagem.

---

## 3.2.6 Verificar o SHA-256

**Objetivo:** confirmar que o arquivo baixado corresponde à imagem publicada.

No diretório em que os dois arquivos foram armazenados:

```bash
cd ~/Downloads
```

Execute:

```bash
sha256sum -c rhel-rhcsa-base-v1.qcow2.sha256
```

Resultado esperado:

```text
rhel-rhcsa-base-v1.qcow2: OK
```

Se aparecer:

```text
FAILED
```

ou qualquer erro de checksum, não utilize a imagem.

Faça novamente o download e repita a verificação.

O checksum protege contra corrupção acidental do arquivo e também permite detectar se o arquivo baixado é diferente daquele utilizado para gerar a assinatura publicada pelo projeto.

---

## 3.2.7 Verificar a estrutura QCOW2

Além do checksum, valide a estrutura interna da imagem:

```bash
qemu-img check ~/Downloads/rhel-rhcsa-base-v1.qcow2
```

Resultado esperado:

```text
No errors were found on the image.
```

Confira também as informações da imagem:

```bash
qemu-img info ~/Downloads/rhel-rhcsa-base-v1.qcow2
```

A imagem utilizada neste projeto possui tamanho virtual de aproximadamente:

```text
30 GiB
```

O tamanho efetivamente ocupado no disco pode ser consideravelmente menor devido ao formato QCOW2 e à compressão.

---

## 3.2.8 Preservar uma cópia-mestre

É recomendável separar a imagem-base dos discos utilizados pelas VMs.

Crie um diretório específico:

```bash
sudo mkdir -p /var/lib/libvirt/base-images
```

Copie a imagem:

```bash
sudo cp \
  ~/Downloads/rhel-rhcsa-base-v1.qcow2 \
  /var/lib/libvirt/base-images/
```

Proteja a cópia contra alterações acidentais:

```bash
sudo chmod 0444 \
  /var/lib/libvirt/base-images/rhel-rhcsa-base-v1.qcow2
```

Confira:

```bash
ls -lh \
  /var/lib/libvirt/base-images/rhel-rhcsa-base-v1.qcow2
```

A partir deste ponto, utilize:

```text
/var/lib/libvirt/base-images/rhel-rhcsa-base-v1.qcow2
```

como origem das novas VMs.

Não inicialize uma VM diretamente a partir desse arquivo.

---

## 3.2.9 Definir os caminhos utilizados pelo procedimento

Para reduzir erros de digitação, defina:

```bash
BASE_IMAGE=/var/lib/libvirt/base-images/rhel-rhcsa-base-v1.qcow2
IMAGE_DIR=/var/lib/libvirt/images
```

Confira:

```bash
echo "$BASE_IMAGE"
echo "$IMAGE_DIR"
```

Valide novamente:

```bash
sudo qemu-img check "$BASE_IMAGE"
```

---

## 3.2.10 Criar os discos independentes das três VMs

Neste projeto são utilizadas cópias completas e independentes.

Não são utilizados backing files ou linked clones neste procedimento.

Essa decisão torna cada VM independente da imagem-base e simplifica cópias, backups, snapshots e movimentação do laboratório entre hospedeiros.

Crie o disco do `bastion`:

```bash
sudo qemu-img convert \
  -p \
  -O qcow2 \
  "$BASE_IMAGE" \
  "$IMAGE_DIR/bastion.qcow2"
```

Crie o disco do `servera`:

```bash
sudo qemu-img convert \
  -p \
  -O qcow2 \
  "$BASE_IMAGE" \
  "$IMAGE_DIR/servera.qcow2"
```

Crie o disco do `serverb`:

```bash
sudo qemu-img convert \
  -p \
  -O qcow2 \
  "$BASE_IMAGE" \
  "$IMAGE_DIR/serverb.qcow2"
```

Atualize o pool:

```bash
sudo virsh -c qemu:///system pool-refresh default
```

---

## 3.2.11 Validar os três discos de sistema

Execute:

```bash
sudo qemu-img check "$IMAGE_DIR/bastion.qcow2"
sudo qemu-img check "$IMAGE_DIR/servera.qcow2"
sudo qemu-img check "$IMAGE_DIR/serverb.qcow2"
```

Os três comandos devem retornar:

```text
No errors were found on the image.
```

Confira o tamanho virtual:

```bash
sudo qemu-img info "$IMAGE_DIR/bastion.qcow2"
sudo qemu-img info "$IMAGE_DIR/servera.qcow2"
sudo qemu-img info "$IMAGE_DIR/serverb.qcow2"
```

Cada disco deve apresentar aproximadamente:

```text
virtual size: 30 GiB
```

---

## 3.2.12 Criar os discos adicionais do servera

Os exercícios de armazenamento utilizam discos separados do sistema operacional.

Crie:

```bash
sudo qemu-img create \
  -f qcow2 \
  "$IMAGE_DIR/servera-vdb.qcow2" \
  5G
```

```bash
sudo qemu-img create \
  -f qcow2 \
  "$IMAGE_DIR/servera-vdc.qcow2" \
  5G
```

```bash
sudo qemu-img create \
  -f qcow2 \
  "$IMAGE_DIR/servera-vdd.qcow2" \
  3G
```

```bash
sudo qemu-img create \
  -f qcow2 \
  "$IMAGE_DIR/servera-vde.qcow2" \
  2G
```

Esses discos devem permanecer vazios.

Não crie partições ou sistemas de arquivos neles.

---

## 3.2.13 Criar os discos adicionais do serverb

Execute:

```bash
sudo qemu-img create \
  -f qcow2 \
  "$IMAGE_DIR/serverb-vdb.qcow2" \
  5G
```

```bash
sudo qemu-img create \
  -f qcow2 \
  "$IMAGE_DIR/serverb-vdc.qcow2" \
  3G
```

---

## 3.2.14 Ajustar contexto de segurança quando aplicável

Em hospedeiros RHEL, Rocky Linux ou outras distribuições que utilizem SELinux, restaure os contextos dos arquivos:

```bash
if command -v restorecon >/dev/null 2>&1; then
  sudo restorecon -RFv /var/lib/libvirt/images
fi
```

Não desabilite SELinux para fazer o laboratório funcionar.

Da mesma forma, em hospedeiros Ubuntu, não desabilite o AppArmor do libvirt.

> Não force `chown qemu:qemu` de forma indiscriminada. O usuário utilizado pelo QEMU varia entre distribuições. Deixe o libvirt gerenciar as permissões e os rótulos sempre que possível.

---

## 3.2.15 Criar a VM bastion

Execute:

```bash
sudo virt-install \
  --connect qemu:///system \
  --name bastion \
  --memory 2048 \
  --vcpus 2 \
  --cpu host \
  --osinfo detect=on,require=off \
  --disk path="$IMAGE_DIR/bastion.qcow2",format=qcow2,bus=virtio \
  --network network=rhcsa-lab,model=virtio \
  --import \
  --graphics vnc,listen=127.0.0.1 \
  --noautoconsole
```

Confirme:

```bash
sudo virsh -c qemu:///system list --all
```

Confira o disco:

```bash
sudo virsh -c qemu:///system domblklist bastion
```

Confira a interface:

```bash
sudo virsh -c qemu:///system domiflist bastion
```

---

## 3.2.16 Criar a VM servera

Execute:

```bash
sudo virt-install \
  --connect qemu:///system \
  --name servera \
  --memory 3072 \
  --vcpus 2 \
  --cpu host \
  --osinfo detect=on,require=off \
  --disk path="$IMAGE_DIR/servera.qcow2",format=qcow2,bus=virtio \
  --disk path="$IMAGE_DIR/servera-vdb.qcow2",format=qcow2,bus=virtio \
  --disk path="$IMAGE_DIR/servera-vdc.qcow2",format=qcow2,bus=virtio \
  --disk path="$IMAGE_DIR/servera-vdd.qcow2",format=qcow2,bus=virtio \
  --disk path="$IMAGE_DIR/servera-vde.qcow2",format=qcow2,bus=virtio \
  --network network=rhcsa-lab,model=virtio \
  --import \
  --graphics vnc,listen=127.0.0.1 \
  --noautoconsole
```

Confira:

```bash
sudo virsh -c qemu:///system domblklist servera
```

A ordem esperada é:

```text
vda   disco do sistema   30 GiB
vdb   laboratório         5 GiB
vdc   laboratório         5 GiB
vdd   laboratório         3 GiB
vde   laboratório         2 GiB
```

---

## 3.2.17 Criar a VM serverb

Execute:

```bash
sudo virt-install \
  --connect qemu:///system \
  --name serverb \
  --memory 2048 \
  --vcpus 2 \
  --cpu host \
  --osinfo detect=on,require=off \
  --disk path="$IMAGE_DIR/serverb.qcow2",format=qcow2,bus=virtio \
  --disk path="$IMAGE_DIR/serverb-vdb.qcow2",format=qcow2,bus=virtio \
  --disk path="$IMAGE_DIR/serverb-vdc.qcow2",format=qcow2,bus=virtio \
  --network network=rhcsa-lab,model=virtio \
  --import \
  --graphics vnc,listen=127.0.0.1 \
  --noautoconsole
```

Confira:

```bash
sudo virsh -c qemu:///system domblklist serverb
```

A ordem esperada é:

```text
vda   disco do sistema   30 GiB
vdb   laboratório         5 GiB
vdc   laboratório         3 GiB
```

---

## 3.2.18 Confirmar as três máquinas virtuais

Execute:

```bash
sudo virsh -c qemu:///system list --all
```

Devem existir:

```text
bastion
servera
serverb
```

Confira as interfaces:

```bash
sudo virsh -c qemu:///system domiflist bastion
sudo virsh -c qemu:///system domiflist servera
sudo virsh -c qemu:///system domiflist serverb
```

Cada interface deve possuir seu próprio endereço MAC.

Não configure o mesmo endereço MAC manualmente em duas VMs.

Quando o parâmetro `mac=` não é especificado, o libvirt gera endereços individuais para os domínios.

---

## 3.2.19 Primeiro boot

A imagem-base foi preparada para gerar novas identidades durante o primeiro boot.

Inicialize inicialmente uma VM de cada vez para facilitar a validação.

Comece pelo `bastion`:

```bash
sudo virsh -c qemu:///system start bastion
```

Confirme:

```bash
sudo virsh -c qemu:///system list
```

Depois faça o mesmo com:

```bash
sudo virsh -c qemu:///system start servera
sudo virsh -c qemu:///system start serverb
```

Se o `virt-install` já tiver deixado alguma VM em execução, não é necessário iniciá-la novamente.

---

## 3.2.20 Identificar o endereço DHCP temporário

Antes da configuração dos IPs definitivos, as VMs podem receber endereços do DHCP da rede `rhcsa-lab`.

Consulte:

```bash
sudo virsh -c qemu:///system net-dhcp-leases rhcsa-lab
```

Também é possível consultar individualmente:

```bash
sudo virsh -c qemu:///system domifaddr bastion
sudo virsh -c qemu:///system domifaddr servera
sudo virsh -c qemu:///system domifaddr serverb
```

Esses endereços são temporários.

Os endereços definitivos serão:

```text
bastion   192.168.100.10/24
servera   192.168.100.11/24
serverb   192.168.100.12/24
```

Eles serão configurados na etapa 04.

---

## 3.2.21 Validar a identidade de cada sistema

A imagem-base não deve transportar a mesma identidade de máquina para todos os clones.

Dentro de cada VM, execute:

```bash
cat /etc/machine-id
```

Anote o valor de cada máquina.

Os três valores devem ser diferentes.

Exemplo conceitual:

```text
bastion   <machine-id A>
servera   <machine-id B>
serverb   <machine-id C>
```

Nunca devem ser:

```text
A = B = C
```

Se duas ou mais VMs apresentarem o mesmo `machine-id`, interrompa a implantação e não avance para os laboratórios.

---

## 3.2.22 Validar as chaves SSH do host

Dentro de cada VM:

```bash
sudo ls -l /etc/ssh/ssh_host_*
```

As chaves devem existir após o primeiro boot.

Consulte a impressão digital da chave ED25519:

```bash
sudo ssh-keygen \
  -lf /etc/ssh/ssh_host_ed25519_key.pub
```

Repita nas três máquinas.

As fingerprints devem ser diferentes.

Isso garante que as VMs não compartilham a mesma identidade SSH.

Se as chaves não existirem:

```bash
sudo ssh-keygen -A
sudo systemctl restart sshd
```

Depois repita a validação.

---

## 3.2.23 Verificar o estado do Red Hat Subscription Management

A imagem-base não deve transportar uma identidade ativa de assinatura pertencente ao sistema utilizado para criá-la.

Dentro de cada VM:

```bash
sudo subscription-manager identity
```

Antes do registro individual, não deve existir uma identidade RHSM herdada da imagem-base.

Se uma identidade válida do sistema original aparecer, não considere a imagem corretamente sanitizada.

Não publique nem replique essa imagem até corrigir o processo de preparação.

---

## 3.2.24 Registrar cada VM individualmente, quando necessário

O laboratório pode utilizar:

- repositórios autorizados através do Red Hat Subscription Management; ou
- a mídia DVD local, conforme descrito na etapa 04.

Se optar pelo Red Hat Subscription Management, registre **cada VM individualmente**.

Não registre a imagem-base.

Exemplo interativo:

```bash
sudo subscription-manager register
```

Após o registro:

```bash
sudo subscription-manager identity
```

Cada VM deve possuir sua própria identidade.

Não inclua nomes de usuário, senhas, tokens ou activation keys no repositório Git.

Se o laboratório utilizar exclusivamente o repositório local da ISO/DVD, prossiga para a etapa 04 sem registrar as VMs neste momento.

---

## 3.2.25 Validar os discos dentro do bastion

No `bastion`:

```bash
lsblk
```

Resultado esperado:

```text
vda    30G
```

Confira também:

```bash
lsblk -f
```

---

## 3.2.26 Validar os discos dentro do servera

No `servera`:

```bash
lsblk
```

Esperado:

```text
vda    30G
vdb     5G
vdc     5G
vdd     3G
vde     2G
```

Os discos:

```text
vdb
vdc
vdd
vde
```

devem permanecer disponíveis para os laboratórios.

Confira:

```bash
lsblk -f
```

Eles não devem conter sistemas de arquivos criados pela implantação.

---

## 3.2.27 Validar os discos dentro do serverb

No `serverb`:

```bash
lsblk
```

Esperado:

```text
vda    30G
vdb     5G
vdc     3G
```

Confira:

```bash
lsblk -f
```

Os discos adicionais devem permanecer sem uso.

---

## 3.2.28 Não alterar a imagem-base depois da implantação

Depois que as cópias forem criadas, a imagem:

```text
/var/lib/libvirt/base-images/rhel-rhcsa-base-v1.qcow2
```

não participa da execução das VMs.

Essa é uma característica intencional do projeto.

As VMs utilizam:

```text
/var/lib/libvirt/images/bastion.qcow2
/var/lib/libvirt/images/servera.qcow2
/var/lib/libvirt/images/serverb.qcow2
```

Por isso, alterações futuras em uma VM não modificam a imagem-base.

Também significa que a imagem-base pode ser utilizada novamente para reconstruir o laboratório.

---

## 3.2.29 Verificar que não existem backing files

O Método B utiliza discos completos e independentes.

Confira:

```bash
sudo qemu-img info --backing-chain \
  /var/lib/libvirt/images/bastion.qcow2
```

Repita:

```bash
sudo qemu-img info --backing-chain \
  /var/lib/libvirt/images/servera.qcow2
```

```bash
sudo qemu-img info --backing-chain \
  /var/lib/libvirt/images/serverb.qcow2
```

Cada comando deve apresentar somente o próprio disco.

Não deve existir dependência da imagem:

```text
rhel-rhcsa-base-v1.qcow2
```

---

## 3.2.30 Problemas comuns

### A imagem falhou na verificação SHA-256

Não utilize o arquivo.

Remova a cópia incorreta e realize novamente o download.

Depois:

```bash
sha256sum -c rhel-rhcsa-base-v1.qcow2.sha256
```

Só prossiga quando o resultado for:

```text
OK
```

### `qemu-img check` encontrou erros

Não tente construir as VMs a partir de uma imagem estruturalmente inconsistente.

Utilize outra cópia da imagem-base.

### A VM já existe

Confira:

```bash
sudo virsh -c qemu:///system list --all
```

Não sobrescreva uma VM existente sem verificar se ela contém dados ou snapshots que precisam ser preservados.

### A rede `rhcsa-lab` não existe

Confira:

```bash
sudo virsh -c qemu:///system net-list --all
```

Retorne para:

[02 — Preparação do host KVM/libvirt](02-host-kvm.md)

### Erro de permissão ao acessar o QCOW2

Confira:

```bash
ls -lhZ /var/lib/libvirt/images/
```

Em host com SELinux:

```bash
sudo restorecon -RFv /var/lib/libvirt/images
```

Não desabilite SELinux para contornar o problema.

Em Ubuntu, consulte também os logs do libvirt e as políticas AppArmor antes de modificar permissões manualmente.

### O host não suporta SPICE

Este procedimento utiliza VNC:

```text
--graphics vnc,listen=127.0.0.1
```

Não é necessário utilizar SPICE para executar o laboratório.

### `virsh domifaddr` não mostra o endereço

Consulte os leases diretamente:

```bash
sudo virsh -c qemu:///system net-dhcp-leases rhcsa-lab
```

Também é possível acessar o console da VM através de `virt-manager`, `virt-viewer` ou Cockpit.

### As SSH host keys são iguais

Não avance.

A imagem ou os clones não foram individualizados corretamente.

Confira:

```bash
sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

em cada VM.

### O `machine-id` é igual em mais de uma VM

Não avance.

O arquivo:

```text
/etc/machine-id
```

deve representar uma identidade individual por máquina.

Uma imagem destinada a clonagem deve ser preparada antes da geração das cópias.

### O Subscription Manager mostra a identidade da VM original

Não considere essa imagem apta para distribuição ou clonagem.

A identidade RHSM da máquina utilizada para construir o template precisa ser removida antes da publicação da imagem-base.

---

## 3.2.31 Como a imagem-base é preparada

Esta seção documenta o processo utilizado pelo mantenedor do projeto para construir uma imagem destinada à clonagem.

Ela não precisa ser repetida por quem apenas utiliza uma imagem-base já validada.

Antes da sanitização, o sistema utilizado como origem deve ser desregistrado:

```bash
sudo subscription-manager unregister
sudo subscription-manager clean
```

Quando aplicável, remova também conexões adicionais associadas à máquina original.

A VM é então desligada.

No host KVM, a sanitização pode ser realizada com `virt-sysprep`.

O procedimento utilizado na preparação desta imagem inclui:

```bash
sudo virt-sysprep \
  -a /var/lib/libvirt/images/rhel-rhcsa-sanitize.qcow2 \
  --operations \
bash-history,dhcp-client-state,logfiles,machine-id,net-hostname,ssh-hostkeys,ssh-userdir,tmp-files,utmp
```

As operações utilizadas removem informações que não devem ser replicadas para as novas VMs, incluindo:

```text
histórico de shell
estado antigo de DHCP
logs da máquina de origem
machine-id
hostname da máquina de origem
SSH host keys
dados SSH dos usuários
arquivos temporários
registros de login
```

Após o `virt-sysprep`, a imagem não deve ser inicializada novamente antes da geração da versão distribuível.

Valide:

```bash
sudo qemu-img check \
  /var/lib/libvirt/images/rhel-rhcsa-sanitize.qcow2
```

A versão final pode ser produzida com:

```bash
sudo qemu-img convert \
  -p \
  -O qcow2 \
  -c \
  /var/lib/libvirt/images/rhel-rhcsa-sanitize.qcow2 \
  rhel-rhcsa-base-v1.qcow2
```

Em seguida:

```bash
qemu-img check rhel-rhcsa-base-v1.qcow2
```

E:

```bash
sha256sum rhel-rhcsa-base-v1.qcow2 \
  > rhel-rhcsa-base-v1.qcow2.sha256
```

A imagem e o arquivo `.sha256` formam o conjunto mínimo necessário para uma distribuição verificável.

---

## 3.2.32 Segurança da imagem-base

Antes da publicação de uma nova versão da imagem, o mantenedor deve confirmar que ela não contém:

```text
chaves SSH privadas pessoais
authorized_keys pessoais
tokens de GitHub
credenciais de nuvem
senhas armazenadas em arquivos de configuração
activation keys
tokens RHSM
identidade de assinatura da VM de origem
histórico contendo segredos
arquivos pessoais
dados de outros projetos
```

Arquivos de imagem RHEL e mídias ISO não devem ser adicionados ao Git.

O Git deve armazenar apenas documentação, automação e código do projeto.

---

## 3.2.33 Compatibilidade com a versão atual do laboratório

A imagem-base descrita nesta documentação utiliza:

```text
RHEL 9.8
```

como sistema operacional local.

O projeto utiliza RHEL 10 como referência de conteúdo para estudo e classificação das competências.

A utilização de RHEL 9.8 localmente não significa que todos os comportamentos sejam idênticos ao RHEL 10.

Os exercícios do projeto devem continuar respeitando a classificação de compatibilidade documentada no repositório.

---

## 3.2.34 Critério para concluir o Método B

Antes de prosseguir, confirme:

```text
[ ] checksum SHA-256 da imagem validado
[ ] qemu-img check sem erros

[ ] imagem-base preservada e não utilizada diretamente por uma VM

[ ] bastion possui disco independente
[ ] servera possui disco independente
[ ] serverb possui disco independente

[ ] não existem backing files entre os discos das VMs e a imagem-base

[ ] bastion existe no libvirt
[ ] servera existe no libvirt
[ ] serverb existe no libvirt

[ ] cada VM possui endereço MAC diferente
[ ] cada VM possui machine-id diferente
[ ] cada VM possui SSH host keys diferentes

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

[ ] discos adicionais permanecem sem uso
[ ] nenhuma identidade RHSM antiga foi herdada da imagem-base
[ ] nenhuma credencial pessoal foi incorporada à imagem
```

Se todos os itens forem atendidos, o Método B está concluído.

A próxima etapa configura os nomes e os endereços IP definitivos das três VMs.

Continue para:

[04 — Configuração inicial das VMs](04-configuracao-vms.md)

[Criação das VMs](03-criacao-vms.md) · [Índice](README.md) · [Home](../../README.md) · [Anterior](03a-instalacao-manual.md) · [Próximo](04-configuracao-vms.md)