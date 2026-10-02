# Hotfix 0.6.1

Correções:

- o grader de `obj01-04` inspeciona `/home/labuser` com `sudo -n`, sem depender das permissões do diretório pessoal do usuário;
- `labctl/runner.py` agora diferencia corretamente:
  - `rc=1` + JSON válido: laboratório incompleto;
  - traceback/erro interno + ausência de JSON: falha real do grader, com diagnóstico útil.

Validação:

```bash
lab --version
bash tests/release-gate.sh
bash tests/integration-reference.sh obj01-04 obj01-05 obj01-06 obj01-07
```
