# Matriz de compatibilidade

O laboratório executa localmente em RHEL 9.8, mas o alvo de estudo é o RHCSA / EX200 baseado em RHEL 10.

Cada exercício deverá declarar um nível de compatibilidade:

| Nível | Significado |
|---|---|
| `exact` | execução equivalente em RHEL 9.8 e RHEL 10 |
| `near` | objetivo válido, mas com diferença relevante entre versões |
| `rhel10-only` | validar em ambiente RHEL 10 |

Exemplo futuro:

```yaml
compatibility:
  local_platform: "RHEL 9.8"
  exam_target: "RHEL 10"
  level: exact
```
