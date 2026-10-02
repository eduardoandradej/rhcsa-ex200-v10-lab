# Entrega 2E — aceleração do Objective 01

Versão: `0.6.0`

Novos labs executáveis:

- `obj01-04` — SSH e troca de usuários
- `obj01-05` — tar, gzip e bzip2
- `obj01-06` — edição de texto com Vim
- `obj01-07` — hard links e symbolic links

Também foram adicionados:

- correções das soluções de referência de `obj01-02` e `obj01-03`;
- `tests/reference-solutions/`;
- `tests/integration-reference.sh`;
- contrato mais rigoroso para labs com status `ready`.

Validação rápida:

```bash
bash tests/release-gate.sh
bash tests/integration-reference.sh obj01-04 obj01-05 obj01-06 obj01-07
```
