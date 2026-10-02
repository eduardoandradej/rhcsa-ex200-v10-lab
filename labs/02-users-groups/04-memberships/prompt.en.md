On `servera`:

1. Add `teamuser1` to supplementary group `projecta`.
2. Add `teamuser2` to supplementary group `projecta`.
3. Change `teamuser2`'s primary group to `projectb`.
4. As `teamuser1`, use `newgrp projecta` to start a shell with `projecta` as the current group.
5. In that shell, create `/home/teamuser1/projecta-owned.txt`.
6. The file must be owned by user `teamuser1` and group `projecta`.

Keep `teamuser1`'s private group as its default primary group.
