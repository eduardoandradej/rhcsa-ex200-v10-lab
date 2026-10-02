No `servera`:

1. Crie `linuxops` com GID `33010`.
2. Crie `auditteam` sem especificar GID.
3. Crie `devtemp` com GID `33021`.
4. Renomeie `devtemp` para `devopsgrp`.
5. Altere o GID de `devopsgrp` para `33022`.
6. Crie `oldgrp` e depois remova esse grupo.

Ao final, `linuxops`, `auditteam` e `devopsgrp` devem existir; `oldgrp` e `devtemp` não.
