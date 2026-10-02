No `servera`, use privilégios administrativos para:

1. Criar `opsalpha` com UID `2301`, comentário `Operations Alpha` e shell `/bin/bash`.
2. Criar `opsbeta` com comentário `Operations Beta`.
3. Alterar o home de `opsbeta` para `/srv/opsbeta` movendo o conteúdo do home atual.
4. Criar `opstemp` e depois removê-lo junto com seu diretório home.
5. Ao final, `opsalpha` e `opsbeta` devem existir e `opstemp` não deve existir.

Não edite `/etc/passwd` manualmente.
