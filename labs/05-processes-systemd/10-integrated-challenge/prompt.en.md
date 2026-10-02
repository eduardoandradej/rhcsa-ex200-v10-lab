## Integrated challenge — Processes, priority, TuneD, and systemd

On `serverb`, work in `/home/student/rhcsa-lab/obj05-10`.

The environment contains:

- CPU-intensive process `rhcsa-rogue-cpu`, already running;
- executable `assets/batch-worker`;
- `rhcsa-api.service`, initially inactive/disabled;
- `rhcsa-legacy.service`, initially active/enabled;
- TuneD prepared for a profile change.

### Tasks

1. Identify `rhcsa-rogue-cpu`.
2. Before terminating it, save:
   `ps -o pid=,%cpu=,%mem=,ni=,stat=,args=`
   to `output/rogue-before.txt`.
3. Terminate `rhcsa-rogue-cpu` with `SIGTERM`.
4. Start `assets/batch-worker` in the background with nice value **10**.
5. Save `$!` to `output/batch.pid`.
6. Leave `rhcsa-api.service` **active and enabled**.
7. Leave `rhcsa-legacy.service` **inactive and masked**.
8. Activate TuneD profile `balanced`.
9. Save `tuned-adm active` to `output/tuned-active.txt`.

### Required final state

```text
rhcsa-rogue-cpu       absent
batch-worker          running with NI=10
rhcsa-api.service     active + enabled
rhcsa-legacy.service  inactive + masked
TuneD                 balanced
```

The grader uses live PIDs and system state; do not hardcode results.
