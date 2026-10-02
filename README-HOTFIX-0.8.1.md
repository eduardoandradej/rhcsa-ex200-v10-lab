# Hotfix 0.8.1 — Grader CLI contract

## Causa

O comando `lab grade` invoca cada grader com a opção `--json`.

Os novos graders de `obj02-01` até `obj02-08` compilavam corretamente, mas
não declaravam essa opção no `argparse`. Por isso o `release-gate` anterior
passou, enquanto a integração falhou antes mesmo de o grader executar.

## Correções

- Todos os oito graders de Objective 02 aceitam `--json`.
- O `release-gate.sh` agora valida explicitamente esse contrato em todos os
  graders `ready`, usando AST em vez de apenas procurar texto.
- Versão atualizada para `0.8.1`.

## Validação recomendada

```bash
bash tests/release-gate.sh
bash tests/integration-objective02.sh
```

Não é necessário repetir Objective 01 neste momento.
