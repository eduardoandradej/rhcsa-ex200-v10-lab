On `servera`, work in `/home/student/rhcsa-lab/obj05-05`.

Two executables are prepared:

```text
assets/nice-start
assets/nice-change
```

Tasks:

1. Start `nice-start` in the background with nice value **12**.
2. Save its PID to `output/nice-start.pid`.
3. Start `nice-change` normally in the background.
4. Save its PID to `output/nice-change.pid`.
5. Use `renice` to change `nice-change` to nice value **7**.
6. Save `ps -o pid=,ni=,stat=,args=` for both processes to
   `output/priorities.txt`.

Leave both processes running at the end.
