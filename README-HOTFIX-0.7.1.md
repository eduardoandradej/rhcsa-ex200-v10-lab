# Hotfix 0.7.1 — SSH servera -> serverb

Causa corrigida:

```text
Host key verification failed.
```

O `obj01-10` dependia de SSH de `servera` para `serverb`, mas essa relação de
confiança ainda não fazia parte da infraestrutura do lab.

Correções:

- `obj01-04` e `obj01-10` preparam chave SSH do `student` de servera para serverb;
- `known_hosts` é atualizado com as chaves atuais do serverb;
- o setup valida SSH com `BatchMode=yes`;
- o solver de referência de `obj01-04` agora usa SSH real;
- o solver de `obj01-10` executa a shell remota com `-Eeuo pipefail`, para que
  uma falha intermediária não seja mascarada por um comando posterior.

Validação:

```bash
bash tests/release-gate.sh
bash tests/integration-reference.sh obj01-04 obj01-10
```
