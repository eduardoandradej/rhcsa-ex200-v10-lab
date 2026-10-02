# Hotfix 0.6.5 — baseline de dependências

Esta entrega introduz a preparação obrigatória das três VMs antes dos labs.

Novos arquivos:

```text
docs/PREREQUISITES.md
ansible/vars/lab_dependencies.yml
ansible/playbooks/00-bootstrap-dependencies.yml
ansible/playbooks/00-validate-dependencies.yml
bootstrap/20-install-dependencies.sh
```

Uso:

```bash
cd ~/rhcsa-ex200-v10-lab
bash bootstrap/20-install-dependencies.sh
```

Depois da mensagem:

```text
DEPENDENCY BASELINE: READY
```

crie/atualize o snapshot base das VMs e somente então execute os labs.
