On `servera`, work in `/home/student/rhcsa-lab/obj05-06`.

The TuneD service is prepared for the exercise.

Tasks:

1. Save `tuned-adm recommend` to `output/recommended.txt`.
2. Save `tuned-adm list` to `output/profiles.txt`.
3. Activate:
   `throughput-performance`
4. Save `tuned-adm active` to `output/active.txt`.
5. Run `tuned-adm verify` and save its output to `output/verify.txt`.

Final state: active profile must be `throughput-performance`.

**Note:** `tuned-adm verify` is diagnostic. Depending on the VM/hardware and
profile characteristics, it can return a non-zero exit status even when the
requested profile is correctly active. Preserve its output and verify the
active profile separately.

`lab finish` restores the previous profile and service state.
