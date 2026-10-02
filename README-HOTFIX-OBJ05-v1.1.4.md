# OBJ05 hotfix v1.1.4

Cumulative over v1.1.1, v1.1.2 and v1.1.3.

## Cause of obj05-03 failure

The setup playbook runs with `become: true`. In v1.1.3, the disposable
`rhcsa-signal-*` processes were therefore started as `root`.

The reference solver intentionally runs the process-control task as `student`.
Linux correctly rejected the signal with:

`Operation not permitted`

This was a setup ownership bug.

## Corrected ownership model

The processes that the exercise expects `student` to control are now actually
created as `student`:

- obj05-03: rhcsa-signal-alpha/beta/gamma
- obj05-04: rhcsa-cpu-hog / rhcsa-mem-hog
- obj05-10: rhcsa-rogue-cpu

PID files stay root-owned and readable in `/run`.

This also proactively fixes the same permission defect that would otherwise
appear later in obj05-04 and obj05-10.

## Retest

```bash
bash tests/validate-obj05-hotfix.sh
bash tests/integration-reference.sh obj05-03
```

If 100%:

```bash
bash tests/integration-objective05.sh
```
