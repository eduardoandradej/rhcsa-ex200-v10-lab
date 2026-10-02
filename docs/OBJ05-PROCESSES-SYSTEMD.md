# Objective 05 — Processes, Scheduling, Tuning & systemd

## Scope

This objective combines the process-management material from RH199 Chapter 9
with systemd service management from Chapter 10, plus two items that are
explicitly listed in the current EX200 objectives:

- adjust process scheduling;
- manage tuning profiles.

## Labs

| Lab | Main skill |
|---|---|
| obj05-01 | `ps`, PID, PPID, STAT, NI |
| obj05-02 | background jobs and job control |
| obj05-03 | SIGSTOP, SIGTERM, SIGCONT |
| obj05-04 | identify CPU/memory intensive processes and terminate them |
| obj05-05 | `nice` and `renice` |
| obj05-06 | `tuned-adm` and tuning profiles |
| obj05-07 | systemd unit/service inventory and state |
| obj05-08 | start, restart, reload |
| obj05-09 | enable, disable, mask, dependencies |
| obj05-10 | integrated EX200-style process/systemd challenge |

## Safety design

The lab avoids disrupting the control channel:

- it does not stop or restart `sshd`;
- destructive service-control exercises use deterministic custom units;
- process exercises use uniquely named disposable processes;
- `lab finish` removes custom units and processes;
- TuneD exercises record and restore their previous profile and service state.

## Exam-oriented behavior

Graders evaluate live state:

- process existence and process state;
- current nice values;
- active TuneD profile;
- systemd active/enabled/masked state;
- MainPID changes across restart and reload.

This permits multiple valid command sequences while rejecting hard-coded
output-only solutions.
