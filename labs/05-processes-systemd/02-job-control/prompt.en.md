On `servera`, work in `/home/student/rhcsa-lab/obj05-02`.

Use **one Bash session** for the exercise.

Executables already exist:

```text
assets/job-alpha
assets/job-beta
```

Tasks:

1. Start `job-alpha` in the background and save `$!` to `output/alpha.pid`.
2. Start `job-beta` in the background and save `$!` to `output/beta.pid`.
3. Use job control to suspend `job-alpha`.
4. Leave `job-beta` running in the background.
5. Save `jobs -l` to `output/jobs.txt`.
6. Save `ps` output for both PIDs to `output/processes.txt`, using:
   `pid,stat,args`, without a header.

Final state:

- `job-alpha`: stopped (`T`);
- `job-beta`: running/sleeping, but not stopped.

Do not terminate the two processes; `lab finish` cleans them up.
