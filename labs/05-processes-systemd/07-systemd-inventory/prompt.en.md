On `servera`, work in `/home/student/rhcsa-lab/obj05-07`.

Without modifying services, generate:

1. `output/services.txt`
   - all loaded service units, active and inactive.
2. `output/unit-files.txt`
   - all installed unit files of type service.
3. `output/sshd-active.txt`
   - result of `systemctl is-active sshd.service`.
4. `output/sshd-enabled.txt`
   - result of `systemctl is-enabled sshd.service`.
5. `output/chronyd-status.txt`
   - `systemctl status chronyd.service` without a pager.

Goal: distinguish runtime state (`active`) from boot configuration (`enabled`).
