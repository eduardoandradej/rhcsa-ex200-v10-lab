# Hotfix 0.6.3

Melhorias:

- `tests/integration-reference.sh` não oculta mais falhas em `lab start`;
- cada ciclo mostra claramente as etapas `start`, `solution`, `grade` e `finish`;
- falhas informam a etapa e o código de retorno;
- `obj01-05` procura `bzip2` nos repositórios configurados do bastion e,
  como fallback, em `/mnt`, `/media` e `/run/media`;
- `bzip2-libs` também é provisionado quando necessário.
