# 01 — Requisitos e arquitetura

[Índice](README.md) · [Home](../../README.md) · [Próximo](02-host-kvm.md)

Este roteiro começa com um host Linux e termina com o primeiro exercício executado pelo estudante. O provisionamento das VMs é manual; o Ansible entra depois, no bastion, para preparar e avaliar cenários.

## Plataforma e requisitos

A base atual do projeto usa **RHEL 9.8 nas três VMs** e toma **RHEL 10 como referência de estudo**. O playbook `validate.yml` atual exige Red Hat Enterprise Linux 9. Usar RHEL 10 requer revisar essa validação e a compatibilidade dos exercícios; não basta trocar a ISO.

O hospedeiro usado neste projeto é **Ubuntu**, com KVM/libvirt. A instalação real foi confirmada como **Ubuntu 24.04.5 LTS (Noble Numbat)**. O guia apresenta Ubuntu como caminho principal e **Rocky Linux 9.8 como alternativa de hospedeiro**. A distribuição do host não precisa ser igual à das VMs.

## Imagens e downloads oficiais

| Uso | Distribuição / imagem | Link oficial |
|---|---|---|
| Host Ubuntu | Ubuntu 24.04 LTS, ISO AMD64 Desktop ou Server | [Imagens da série 24.04](https://releases.ubuntu.com/24.04/) |
| Host alternativo | Rocky Linux 9.8 x86_64, Minimal ou DVD | [Diretório oficial de ISOs 9.8](https://download.rockylinux.org/pub/rocky/9.8/isos/x86_64/) |
| Host alternativo, instalação mínima | Rocky Linux 9.8 Minimal x86_64 | [Baixar ISO Minimal](https://download.rockylinux.org/pub/rocky/9.8/isos/x86_64/Rocky-9.8-x86_64-minimal.iso) |
| Host alternativo, mídia completa | Rocky Linux 9.8 DVD x86_64 | [Baixar ISO DVD](https://download.rockylinux.org/pub/rocky/9.8/isos/x86_64/Rocky-9.8-x86_64-dvd.iso) |
| VMs da base atual | RHEL 9.8, Binary DVD x86_64 | [Red Hat Developer](https://developers.redhat.com/products/rhel/download) · [Portal de downloads RHEL](https://access.redhat.com/downloads/content/rhel) |

No Ubuntu Desktop há interface gráfica para virt-manager; Ubuntu Server não a inclui. Escolha conforme a forma de gerenciamento do host. Use a ISO da série 24.04 disponível na página oficial, sem confundir a atualização da mídia com a versão exata do host original.

O download RHEL depende do acesso autorizado à conta Red Hat. No portal, selecione RHEL 9.8 e a mídia **Binary DVD x86_64** para reproduzir a base. Links diretos autenticados/temporários da ISO não são publicados no projeto. A ISO Boot depende de uma fonte de pacotes durante a instalação; ela não substitui a DVD no procedimento de repositório local.

Confira checksums nas páginas oficiais: [SHA256SUMS do Ubuntu](https://releases.ubuntu.com/24.04/SHA256SUMS) e [CHECKSUM do Rocky 9.8](https://download.rockylinux.org/pub/rocky/9.8/isos/x86_64/CHECKSUM). Compare o arquivo exato baixado e, para conferir a origem, valide também a assinatura com a chave oficial da distribuição.

### Rocky como host ou como VM?

**Como hospedeiro:** pode executar KVM/libvirt com as VMs RHEL do projeto; siga o caminho Rocky na etapa 2. Essa alternativa está documentada, mas não foi validada neste projeto durante a geração do pacote.

**Como sistema das VMs:** Rocky Linux 9.8 é uma opção para adaptar os exercícios gerais de Linux, mas não é uma substituição automática no projeto atual. O playbook `ansible/playbooks/validate.yml` exige `ansible_distribution == "RedHat"`; com Rocky ele falhará. Também é necessário revisar repositórios, chaves GPG, pacotes e classificações de compatibilidade antes de considerar essa variante validada. Não use a configuração de repositórios RHEL/DVD como se fosse Rocky. A base de referência continua RHEL 9.8 nas VMs.

## Configuração real do hospedeiro

| Item | Registro disponível |
|---|---|
| Equipamento | ThinkPad T430 (identificação informada no terminal do autor) |
| Sistema | Ubuntu 24.04.5 LTS (Noble Numbat), x86_64 |
| Virtualização | KVM/QEMU gerenciado por libvirt |
| Processador | Intel Core i5-3320M, frequência nominal 2,60 GHz; máxima reportada 3,30 GHz |
| Topologia de CPU | 1 socket, 2 núcleos físicos, 2 threads por núcleo: 4 CPUs lógicas |
| Virtualização da CPU | Intel VT-x (`vmx` no resultado de `lscpu`) |
| Memória RAM | 15 GiB reportados por `free -h` |
| Swap | 4,0 GiB |
| Disco físico | SSD Kingston SA400S37240G, capacidade comercial 240 GB; 223,6 GiB exibidos por `lsblk` |
| Tipo de armazenamento | Não rotacional (`ROTA=0` no SSD) |
| Rede das VMs | 192.168.100.0/24; gateway 192.168.100.1 |
| Discos virtuais dos alvos | Sistema 30 GiB; discos extras conforme tabela abaixo |

Configuração registrada a partir da coleta fornecida pelo autor em 02/10/2026. Os 4 processadores lógicos correspondem a **2 núcleos físicos com Hyper-Threading**, não a 4 núcleos físicos. A coleta identifica VT-x; a validação operacional de KVM continua na etapa 2.

Os valores momentâneos de memória usada/disponível não são requisitos do projeto e não foram tratados como capacidade fixa. A coleta não informa o espaço livre do filesystem nem confirma o diretório físico dos discos das VMs. Antes de uma nova instalação, confira `df -h /var/lib/libvirt/images` (ou o caminho real do pool).

A tabela de recursos abaixo é **dimensionamento sugerido para uma nova instalação**, não a alocação medida das VMs atuais. As três VMs propostas somam 7 GiB de RAM e 6 vCPUs; vCPUs são uma alocação compartilhada sobre as 4 CPUs lógicas do host. O desempenho depende da carga simultânea e dos recursos consumidos pelo Ubuntu.

Para conferir a configuração de outro hospedeiro, execute nele:

```bash
cat /etc/os-release
lscpu
free -h
lsblk -d -o NAME,SIZE,MODEL,ROTA
sudo virsh -c qemu:///system net-list --all
sudo virsh -c qemu:///system pool-list --all
```

Não execute a coleta dentro de bastion: ela mostraria os recursos da VM. `ROTA=0` normalmente indica armazenamento não rotacional; `ROTA=1` indica rotacional conforme exposto pelo dispositivo.

Dimensionamento inicial sugerido, não um mínimo certificado:

| Máquina | vCPU | RAM | Disco do sistema | Discos extras |
|---|---:|---:|---:|---|
| bastion | 2 | 2 GiB | 30 GiB | nenhum |
| servera | 2 | 3 GiB | 30 GiB | 5 + 5 + 3 + 2 GiB |
| serverb | 2 | 2 GiB | 30 GiB | 5 + 3 GiB |

Reserve memória para o host; 16 GiB de RAM é uma configuração inicial confortável. Reserve pelo menos 120 GiB livres para sistemas, ISO e crescimento dos snapshots. A necessidade real varia com exercícios e retenção. SSD é preferível.

Pré-requisitos: CPU x86_64 com AMD-V/VT-x habilitado no firmware; host Linux instalado; acesso administrativo; ISO DVD do RHEL obtida legalmente e compatível com a versão das VMs; espaço em disco; conexão para obter o projeto e dependências. A ISO e materiais oficiais não são distribuídos aqui.

## Rede isolada de prática

| Elemento | Endereço | Papel |
|---|---|---|
| Rede libvirt `rhcsa-lab` | 192.168.100.0/24 | NAT do laboratório |
| Interface do host `virbr-rhcsa` | 192.168.100.1 | gateway/DNS das VMs |
| bastion | 192.168.100.10 | estação do aluno e automação |
| servera | 192.168.100.11 | alvo principal |
| serverb | 192.168.100.12 | alvo auxiliar |

Domínio usado no roteiro: `lab.example`. Verifique se 192.168.100.0/24 conflita com LAN, VPN ou outra rede libvirt. Se conflitar, escolha outra faixa e atualize rede, VMs, resolução de nomes e inventário juntos.

O host KVM executa `virsh` e cria as VMs. O bastion executa Git, Ansible e `lab`. As tarefas dos exercícios são resolvidas manualmente em servera/serverb. Não é necessário clonar o projeto no host para seguir as etapas 2 a 4.

**Antes de avançar:** confirme a ISO, os recursos disponíveis e uma faixa de rede sem conflito.

[Índice](README.md) · [Home](../../README.md) · [Próximo](02-host-kvm.md)
