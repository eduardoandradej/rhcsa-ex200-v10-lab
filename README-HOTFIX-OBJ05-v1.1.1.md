# OBJ05 hotfix v1.1.1

Correções:

1. `obj05-01` e `obj05-03`:
   - substitui o uso de `kill -SIGSTOP` dentro de tasks Ansible `shell`;
   - usa `/usr/bin/kill -s STOP`, que não depende da sintaxe do builtin `kill`
     usado pelo `/bin/sh`.

2. `prepare-objective05.yml`:
   - remove o parâmetro `executable` inválido do módulo `command`;
   - valida os comandos com `shell: command -v ...`;
   - elimina o warning observado com Ansible 2.14.

3. Reference solvers:
   - normaliza sinais para `kill -s STOP|TERM|CONT`.

4. `obj05-01` grader:
   - torna a leitura do campo `STAT` mais direta.

5. Novo gate:
   - `tests/release-gate-obj05-portability.sh` impede retorno da forma
     incompatível em YAML do OBJ05.

## Reteste mínimo

```bash
bash tests/validate-obj05-hotfix.sh
bash tests/integration-objective05.sh
```
