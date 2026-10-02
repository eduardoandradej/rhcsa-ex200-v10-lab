On `servera`, three training processes exist:

```text
rhcsa-signal-alpha   initially running
rhcsa-signal-beta    initially running
rhcsa-signal-gamma   initially stopped
```

PIDs are in `/run/rhcsa-signal-*.pid`.

Using **signal names**:

1. send `SIGSTOP` to `alpha`;
2. send `SIGTERM` to `beta`;
3. send `SIGCONT` to `gamma`.

Final state:

- `alpha` exists and is in `T`;
- `beta` no longer exists;
- `gamma` exists and is not in `T`.

Do not use `SIGKILL` in this exercise.
