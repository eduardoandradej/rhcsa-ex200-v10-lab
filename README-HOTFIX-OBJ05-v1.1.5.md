# OBJ05 hotfix v1.1.5

Cumulative over v1.1.1 through v1.1.4.

## obj05-06 reference-solution failure

The reference solver used `set -Eeuo pipefail` and executed:

`tuned-adm verify`

as its final command with output redirected to `output/verify.txt`.

`tuned-adm verify` is diagnostic and may return a non-zero status when it
detects a host/profile deviation. Because the solver was running with `set -e`,
that diagnostic result aborted the reference solution before the grader ran.

## Correction

- preserve `tuned-adm verify` output in `output/verify.txt`;
- preserve its numeric exit status in `output/verify.rc`;
- do not treat that diagnostic rc alone as a reference-solver failure;
- explicitly validate that `throughput-performance` is the active profile;
- update the lab text to teach the distinction.

## Retest

Before applying the hotfix, if the failed lab is still active, you can inspect
the original diagnostic output with:

```bash
cat /home/student/rhcsa-lab/obj05-06/output/verify.txt
```

After applying v1.1.5:

```bash
bash tests/validate-obj05-hotfix.sh
bash tests/integration-reference.sh obj05-06
```

If it passes:

```bash
bash tests/integration-objective05.sh
```
