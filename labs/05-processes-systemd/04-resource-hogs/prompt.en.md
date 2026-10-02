On `servera`, the lab started:

- `rhcsa-cpu-hog` — continuous CPU load;
- `rhcsa-mem-hog` — significant memory allocation.

PIDs:

```text
/run/rhcsa-cpu-hog.pid
/run/rhcsa-mem-hog.pid
```

Work in `/home/student/rhcsa-lab/obj05-04`.

Before terminating the processes:

1. Use `ps` or `top` to investigate CPU and memory.
2. Save the CPU process row to `output/cpu-before.txt`.
3. Save the memory process row to `output/memory-before.txt`.
4. Rows must include at least PID, `%CPU`, `%MEM`, `STAT`, and `ARGS`.

Then terminate both processes with `SIGTERM`.

At the end, neither PID must exist.
