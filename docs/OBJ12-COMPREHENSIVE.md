# Objective 12 — Comprehensive EX200 Challenges

OBJ12 is the final integration layer of the local RHCSA practice environment.
The six exercises are original scenarios built to combine previously isolated
skills. They are not copies of Red Hat course labs or exam questions.

| Lab | Integrated focus |
|---|---|
| obj12-01 | users, groups, password aging, permissions, setgid, ACL, shell |
| obj12-02 | systemd service, cron, tmpfiles, rsyslog |
| obj12-03 | GPT, LVM, XFS growth, persistent mount, swap |
| obj12-04 | default target, grubby, persistent fstab mount |
| obj12-05 | SELinux file/port policy, firewalld, Apache |
| obj12-06 | users, permissions, shell, cron, NFS, indirect AutoFS |

## Exam-style behavior

Prompts describe required final states and evidence rather than prescribing
the exact command sequence. Graders inspect resulting state.

Reference solutions exist only for engineering regression of the lab
framework.

## Safety

- automated OBJ12 labs never reboot a VM;
- `/dev/vda` is forbidden;
- destructive storage is restricted to `/dev/vdb` and uses the existing
  guard/reset framework;
- fstab-changing labs save and restore `/etc/fstab`;
- SELinux is never disabled;
- no `audit2allow`, `no_root_squash`, or firewall shortcuts are used.
