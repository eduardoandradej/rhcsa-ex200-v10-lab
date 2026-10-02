On `servera`, `lab start` created two training processes:

- `rhcsa-proc-sleeper`
- `rhcsa-proc-stopped`

Their PIDs are stored in:

```text
/run/rhcsa-proc-sleeper.pid
/run/rhcsa-proc-stopped.pid
```

Work in `/home/student/rhcsa-lab/obj05-01`.

Using `ps`, generate exactly these two reports:

```text
output/sleeper.txt
output/stopped.txt
```

Each report must use these columns without a header:

```text
PID PPID STAT NI ARGS
```

Use the corresponding PID for each process.

Goal: identify PID, PPID, process state (`STAT`), nice value, and command line. Do not alter or terminate the processes.
