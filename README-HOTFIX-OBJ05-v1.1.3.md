# OBJ05 hotfix v1.1.3

Cumulative over v1.1.1 and v1.1.2.

## Root cause of the obj05-02 60% result

Two different behaviors were exposed:

1. The solver could send STOP before `nohup` and the script finished their
   `exec()` chain. In that race, the PID was still displayed as
   `nohup ./assets/job-alpha`, so the grader correctly rejected it.

2. A stopped process group whose controlling shell exits becomes orphaned.
   Linux sends SIGHUP/SIGCONT to an orphaned stopped process group. Because
   `nohup` ignores SIGHUP, SIGCONT can leave the process running.

## v1.1.3 behavior

The solver now:

- waits for `rhcsa-job-alpha` and `rhcsa-job-beta` to be the real argv;
- performs actual Bash job control and captures `jobs -l` while alpha is stopped;
- captures `ps` while alpha is stopped;
- resumes and disowns both jobs before the first SSH shell exits;
- uses a second SSH session to restore alpha to STOP after the original
  job-control shell has disappeared.

This produces the intended final state without the
`warning: deleting stopped job` message.

Startup-race protection is also applied proactively to obj05-05 and obj05-10.
