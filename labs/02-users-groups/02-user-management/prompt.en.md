On `servera`, use administrative privileges to:

1. Create `opsalpha` with UID `2301`, comment `Operations Alpha`, and shell `/bin/bash`.
2. Create `opsbeta` with comment `Operations Beta`.
3. Change `opsbeta`'s home to `/srv/opsbeta`, moving the existing home contents.
4. Create `opstemp`, then remove it together with its home directory.
5. At the end, `opsalpha` and `opsbeta` must exist and `opstemp` must not exist.

Do not edit `/etc/passwd` manually.
