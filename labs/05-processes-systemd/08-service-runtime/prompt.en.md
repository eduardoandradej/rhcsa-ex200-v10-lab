On `servera`, the lab installed `rhcsa-control.service`, initially inactive
and disabled.

Work in `/home/student/rhcsa-lab/obj05-08`.

Tasks:

1. Start `rhcsa-control.service`.
2. Save `MainPID` to `output/start.pid`.
3. Restart the service.
4. Save the new `MainPID` to `output/restart.pid`.
5. Reload the service.
6. Save `MainPID` after reload to `output/reload.pid`.
7. Leave the service **active** at the end.

Expected concept:

- restart → PID changes;
- reload → main PID does not change.

Do not enable the service at boot in this lab.
