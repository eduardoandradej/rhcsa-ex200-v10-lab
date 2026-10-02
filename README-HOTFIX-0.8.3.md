# Hotfix 0.8.3 — privileged grader paths

## Causa

`/etc/sudoers.d` não é atravessável pelo usuário `student` no cenário do lab.
O estado produzido pelo solver de `obj02-06` estava correto, mas o grader
tentava executar `Path.is_file()` e `Path.stat()` diretamente como `student`.

Isso gerava:

```text
PermissionError: [Errno 13] Permission denied: '/etc/sudoers.d/opsadmin'
```

## Correção

O grader agora inspeciona os objetos privilegiados pelo canal administrativo
do próprio laboratório:

```bash
sudo -n test -f ...
sudo -n stat -c %a ...
sudo -n visudo -cf ...
```

Também foi corrigido preventivamente `obj02-08`, que possuía o mesmo padrão e
falharia ao chegar em `/etc/sudoers.d/consultantsx`.

O `obj02-06` agora valida ainda:

- `id` autorizado sem senha;
- `whoami` autorizado sem senha;
- um comando fora da lista (`hostname`) não autorizado sem senha.

## Próxima validação

```bash
bash tests/integration-reference.sh obj02-06

bash tests/integration-reference.sh   obj02-07 obj02-08
```
