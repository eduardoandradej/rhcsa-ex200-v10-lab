## Integrated challenge — Objective 01

On `servera`, as `student`, work in:

`/home/student/rhcsa-lab/obj01-10`

Do not manually edit files that the instructions require you to produce through commands, filters, or redirections.

1. Create `work/{reports,logs,links,archive}`.
2. Copy `input/report.txt` to `work/reports/final-report.txt`, preserving the original.
3. From `input/systems.txt`, select only `prod` and `active` records and save them to `work/reports/prod-active.txt`.
4. From `input/events.log`, select `WARN` or `ERROR` lines using an extended regular expression and save them to `work/logs/alerts.log`.
5. Save the FQDN of `serverb`, obtained through SSH from `servera`, to `work/reports/remote-host.txt`.
6. Edit `work/reports/final-report.txt` to replace `STATUS=PENDING` with `STATUS=READY`.
7. Set `final-report.txt` to mode `0640` and `work/reports` to `0750`.
8. Create the hard link `work/links/report.hard` for `work/reports/final-report.txt`.
9. Create the symbolic link `work/links/alerts.current` pointing relatively to `../logs/alerts.log`.
10. Create `work/archive/evidence.tar.gz` containing the `reports` and `logs` directories from the `work` tree.
11. Using local documentation, save only the path returned by `man -w chmod` to `work/reports/chmod-manpath.txt`.

When finished:

```bash
lab grade obj01-10
```
