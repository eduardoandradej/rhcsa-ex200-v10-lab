# Entrega 2F — fechamento do Objective 01

Versão: `0.7.0`

Novos labs executáveis:

- `obj01-08` — Permissões de arquivos
- `obj01-09` — Documentação do sistema
- `obj01-10` — Desafio integrado Essential Tools

A regressão padrão agora cobre `obj01-01` até `obj01-10`.

Validação recomendada:

```bash
bash tests/release-gate.sh
bash tests/integration-reference.sh obj01-08 obj01-09 obj01-10
```

Após esses três passarem, execute a regressão integral:

```bash
bash tests/integration-reference.sh
```
