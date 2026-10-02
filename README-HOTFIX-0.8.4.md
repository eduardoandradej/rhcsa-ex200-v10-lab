# Hotfix 0.8.4 — obj02-07 chpasswd setup

## Causa

O `setup.yml` do `obj02-07` enviava várias linhas para `chpasswd` por um
bloco YAML literal. No ambiente executado, o conteúdo chegou ao comando com
uma linha adicional vazia e o `chpasswd` interpretou essa quinta linha como
uma entrada sem senha:

```text
chpasswd: line 5: missing new password
chpasswd: error detected, changes ignored
```

## Correção

A preparação agora define a senha de cada usuário em uma chamada individual
e sem newline adicional:

```yaml
ansible.builtin.command: chpasswd
args:
  stdin: "{{ item }}:redhat"
  stdin_add_newline: false
```

Isso remove a dependência da interpretação de blocos multilinha.

## Validação

```bash
bash tests/integration-reference.sh obj02-07

bash tests/integration-reference.sh obj02-08
```
