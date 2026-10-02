# 06 — Configuração e validação do Ansible

[Índice](README.md) · [Home](../../README.md) · [Anterior](05-bastion-git.md) · [Próximo](07-baseline.md)

**Onde executar:** bastion, como `student`.

## Conferir o inventário existente

```bash
cd ~/rhcsa-ex200-v10-lab/ansible
cat ansible.cfg
cat inventory/hosts.yml
ansible-inventory --graph
```

O inventário atual usa `control` para bastion (conexão local) e `managed` para servera/serverb. Os alvos usam `student` e `/home/student/.ssh/id_ed25519_rhcsa_lab`. Se adotou outra rede, edite os dois `ansible_host` em `inventory/hosts.yml` antes do teste. Execute os comandos nesta pasta: `ansible.cfg` usa caminhos relativos.

```bash
ansible managed -m ansible.builtin.ping
ansible managed -m ansible.builtin.command -a 'hostname -f'
ansible-playbook playbooks/validate.yml
cd ~/rhcsa-ex200-v10-lab
lab status
```

`ansible.builtin.ping` verifica SSH e Python no alvo; não é ICMP. O resultado esperado é sucesso nos dois nós, RHEL 9 na validação e ambiente READY no CLI.

## Privilégios nos cenários

Os primeiros cenários usam o próprio `student`. Cenários com `become: true` precisam de autorização de sudo no alvo. Para usar a automação sem prompt, configure **apenas nas VMs descartáveis de laboratório** uma regra dedicada, via `sudo visudo -f /etc/sudoers.d/rhcsa-lab-student`:

```sudoers
student ALL=(ALL) NOPASSWD: ALL
```

```bash
sudo chmod 440 /etc/sudoers.d/rhcsa-lab-student
sudo visudo -cf /etc/sudoers.d/rhcsa-lab-student
```

Repita nas VMs em que os cenários exigirem elevação. O runner atual não solicita senha de sudo. Esta regra é uma escolha para o laboratório, não uma configuração padrão de produção.

## Falhas comuns

| Sintoma | Verificar |
|---|---|
| No route / timeout | VM ligada, IP, rede libvirt, gateway e firewall |
| Permission denied | usuário, chave dedicada, authorized_keys e ssh-agent |
| Host key verification failed | identidade do host e known_hosts |
| Python/module ausente | Python nos alvos; PyYAML no bastion |
| Inventory vazio/incorreto | diretório atual e ansible.cfg |
| validate.yml rejeita o sistema | baseline atual exige RHEL 9 |
| lab não encontrado | instalação do wrapper e PATH de ~/.local/bin |

**Antes de avançar:** três nós validados; não crie o baseline de um ambiente com falhas.

[Índice](README.md) · [Home](../../README.md) · [Anterior](05-bastion-git.md) · [Próximo](07-baseline.md)
