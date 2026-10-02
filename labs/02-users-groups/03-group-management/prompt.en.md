On `servera`:

1. Create `linuxops` with GID `33010`.
2. Create `auditteam` without specifying a GID.
3. Create `devtemp` with GID `33021`.
4. Rename `devtemp` to `devopsgrp`.
5. Change `devopsgrp`'s GID to `33022`.
6. Create `oldgrp`, then remove it.

At the end, `linuxops`, `auditteam`, and `devopsgrp` must exist; `oldgrp` and `devtemp` must not.
