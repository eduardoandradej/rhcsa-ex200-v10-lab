## Drill manual de console

Este exercício **não é iniciado por `lab start`**. Ele é propositalmente
manual porque exige interação com o menu do GRUB antes de o SSH existir.

No host KVM, use o console do `servera` e pratique um boot temporário em
`emergency.target`:

1. Reinicie `servera`.
2. Interrompa o menu do GRUB e edite apenas a entrada do boot atual.
3. Acrescente `systemd.unit=emergency.target` à linha do kernel.
4. Inicialize usando a entrada temporariamente modificada.
5. Observe o estado do sistema e identifique se `/` está `ro` ou `rw`.
6. Se necessário para manutenção, remonte `/` como leitura/escrita.
7. Compare conceitualmente `emergency.target` com `rescue.target`.
8. Saia do modo de manutenção e retorne ao boot normal.

A modificação feita no editor do GRUB deve afetar **somente esse boot**.

### Limite do laboratório local

O bastion não possui um canal `hostctl` autorizado para controlar o libvirt do
Ubuntu. Automatizar esta etapa exigiria dar ao bastion capacidade de
interromper o boot e controlar o console do hipervisor, aumentando
desnecessariamente a superfície de privilégio. Por isso este item fica como
drill manual e deve ser repetido também no lab RHEL 10 da RHLS.
