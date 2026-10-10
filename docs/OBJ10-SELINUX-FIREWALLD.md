# Objective 10 — SELinux & firewalld

OBJ10 consolidates the RHEL 10 administration skills for SELinux and network
security in nine original hands-on labs.

| Lab | Skill |
|---|---|
| obj10-01 | SELinux mode/process/file-context inventory |
| obj10-02 | current and persistent SELinux mode |
| obj10-03 | persistent file contexts with semanage/restorecon |
| obj10-04 | persistent SELinux Boolean |
| obj10-05 | AVC investigation and context repair |
| obj10-06 | firewalld zone/source/service/port persistence |
| obj10-07 | SELinux labeling of a nonstandard service port |
| obj10-08 | persistent port in the active firewalld zone |
| obj10-09 | integrated Apache + SELinux + firewalld challenge |

## Safety boundary

SELinux is never disabled. A single lab intentionally starts in permissive
mode so that the learner restores enforcing mode; cleanup restores the prior
state.

Firewall labs never remove SSH, change the default zone, or move the
management interface. `obj10-06` uses an isolated custom zone. Labs that touch
the active zone only add one unique training port and remove it during
cleanup.

The reference path does not use `audit2allow` as a shortcut for ordinary
labeling errors.

## Compatibility

The local runtime target remains RHEL 9.8 because of the lab host CPU
constraint. The tasks are graded by final state and by commands/concepts that
map to the current RHEL 10 RHCSA rapid-track material.
