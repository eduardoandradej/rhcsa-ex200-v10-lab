# 07 — Baseline e snapshots

[Índice](README.md) · [Home](../../README.md) · [Anterior](06-validacao-ansible.md) · [Próximo](08-primeiro-lab.md)

**Onde executar:** primeiro bastion; depois host KVM. Os snapshots são operados no host, sem abrir acesso libvirt ao bastion.

`lab finish` executa a limpeza prevista no exercício. Ele **não** reverte automaticamente a VM inteira para um snapshot. O reset integrado via host-control continua no roadmap.

## Preparar baseline consistente

No bastion, confirme que não há exercício ativo:

```bash
lab status
```

Se houver, finalize-o com `lab finish ID_DO_EXERCICIO` e valide de novo. Desligue as três VMs de forma limpa pelo console ou pelo host:

```bash
sudo virsh -c qemu:///system shutdown servera
sudo virsh -c qemu:///system shutdown serverb
sudo virsh -c qemu:///system shutdown bastion
sudo virsh -c qemu:///system list --all
```

Aguarde até todas exibirem `shut off`. Não use `destroy` como substituto normal de desligamento.

Neste roteiro, os discos foram criados em qcow2. Confira o XML e garanta que todos os discos graváveis participam do snapshot, inclusive os discos extras. Se sua VM usa discos raw, passthrough ou outra topologia, não aplique o exemplo sem adaptar o plano de snapshot.

```bash
sudo virsh -c qemu:///system snapshot-list bastion
sudo virsh -c qemu:///system snapshot-list servera
sudo virsh -c qemu:///system snapshot-list serverb
sudo virsh -c qemu:///system snapshot-create-as bastion baseline-pre-labs --description 'Sistema, rede e ferramentas prontos; nenhum lab ativo'
sudo virsh -c qemu:///system snapshot-create-as servera baseline-pre-labs --description 'Alvo limpo com discos de pratica'
sudo virsh -c qemu:///system snapshot-create-as serverb baseline-pre-labs --description 'Alvo auxiliar limpo'
```

Não reutilize o nome se ele já existir. Os exemplos usam snapshots internos da configuração qcow2 desta instalação. Valide o resultado e reinicie:

```bash
sudo virsh -c qemu:///system snapshot-info bastion baseline-pre-labs
sudo virsh -c qemu:///system snapshot-info servera baseline-pre-labs
sudo virsh -c qemu:///system snapshot-info serverb baseline-pre-labs
sudo virsh -c qemu:///system start bastion
sudo virsh -c qemu:///system start servera
sudo virsh -c qemu:///system start serverb
```

Depois da inicialização, execute `lab status` no bastion.

## Restauração manual

A restauração descarta alterações posteriores ao baseline, incluindo arquivos e commits no bastion. Preserve alterações de projeto em Git/backup antes. Desligue as VMs de forma limpa, confirme o estado e só então execute no host:

```bash
sudo virsh -c qemu:///system snapshot-revert servera baseline-pre-labs
sudo virsh -c qemu:///system snapshot-revert serverb baseline-pre-labs
sudo virsh -c qemu:///system snapshot-revert bastion baseline-pre-labs
sudo virsh -c qemu:///system start bastion
sudo virsh -c qemu:///system start servera
sudo virsh -c qemu:///system start serverb
```

Revalidar o estado do CLI é necessário: restaurar somente um alvo durante um exercício deixa o estado local no bastion diferente do cenário remoto. O baseline sincronizado das três VMs evita isso. Um snapshot não substitui backup independente dos discos e da definição das VMs.

**Antes de avançar:** snapshots identificados, VMs ligadas e ambiente validado novamente.

[Índice](README.md) · [Home](../../README.md) · [Anterior](06-validacao-ansible.md) · [Próximo](08-primeiro-lab.md)
