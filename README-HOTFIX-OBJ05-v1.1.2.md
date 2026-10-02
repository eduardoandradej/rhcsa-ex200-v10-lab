# OBJ05 hotfix v1.1.2

This is cumulative over v1.1.1.

## Cause of obj05-02 reference-solution hang

The reference solver launched long-running processes inside a non-interactive
SSH session without redirecting their stdout/stderr.

Those child processes inherited the SSH channel file descriptors. Even after
the shell completed its commands, the SSH channel could remain open while the
background jobs were alive. `obj05-02` is especially sensitive because one job
is deliberately left in a stopped state.

## Fix

- obj05-02:
  - launch both jobs with `nohup`;
  - redirect stdin-independent output away from the SSH channel;
  - collect `jobs -l` and `ps`;
  - `disown` both jobs before the SSH shell exits.

- obj05-05 and obj05-10:
  - proactively apply the same SSH background-process safety pattern.

## Retest

```bash
bash tests/validate-obj05-hotfix.sh
bash tests/integration-reference.sh obj05-02
```

If obj05-02 passes:

```bash
bash tests/integration-objective05.sh
```
