No `servera`, `rhcsa-update-demo-1.0-1` já está instalado.

Existem dois repositórios:

- `rhcsa-base` — habilitado, contém versão `1.0-1`;
- `rhcsa-errata` — desabilitado, contém versão `2.0-1`.

Faça o seguinte:

1. Habilite persistentemente `rhcsa-errata`.
2. Atualize **somente** `rhcsa-update-demo` para a versão disponível mais recente.
3. Verifique a versão instalada com RPM.
4. Ao final, desabilite persistentemente **os dois repositórios customizados**.

Não remova o pacote atualizado.
