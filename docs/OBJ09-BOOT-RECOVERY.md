# Objective 09 — Boot, GRUB & Recovery

OBJ09 is aligned to the current RH199 RHEL 10 coverage of boot-loader
management, kernel command-line arguments, systemd boot targets, boot-time
filesystem troubleshooting, and superuser recovery.

| Lab | Skill | Harness status |
|---|---|---|
| obj09-01 | boot/kernel/GRUB inventory | ready / automated |
| obj09-02 | persistent kernel args with `grubby` | ready / automated |
| obj09-03 | default systemd target | ready / automated |
| obj09-04 | rescue/emergency boot from GRUB | manual-only |
| obj09-05 | fstab recovery workflow | ready / automated |
| obj09-06 | root access recovery from boot loader | manual-only |
| obj09-07 | integrated boot/recovery challenge | ready / automated |

## Why two labs are manual-only

The local training VM is RHEL 9.8 while the certification target and RH199
reference are RHEL 10. The KVM host exposes a working serial console, but the
bastion intentionally has no privileged host-control channel for libvirt.

Automating GRUB-menu interaction would require granting the bastion
out-of-band control of the Ubuntu hypervisor, including the ability to reset
the VM and inject console input before SSH is available. That privilege is not
required for the rest of the project and is deliberately not introduced only
to make the reference regression green.

There is an additional RHEL 10 recovery nuance: the current no-media root
recovery method can require changing `console=` kernel arguments. The local
automation channel itself is the serial console, so changing those arguments
can remove the channel that the automation depends on.

Therefore:

- `obj09-04` and `obj09-06` remain first-class catalog entries but are marked
  `manual-only`;
- they are not included in automated reference integration;
- they should be practiced from a graphical/libvirt console when desired;
- they should be repeated in RHLS Premium on an actual RHEL 10 lab;
- the repository does not bundle Red Hat installation/rescue media.

## Safe adaptation of fstab recovery

`obj09-05` uses a real scratch filesystem and a real `/etc/fstab` entry, but
the initial broken entry includes `nofail`. This prevents an accidental reboot
from trapping the VM before the learner fixes the exercise. The final state
requires removal of `nofail`, a correct UUID-based entry, a successful mount,
and a clean `findmnt --verify`.

## Regression accounting

OBJ09 contains seven learning items:

- five fully automated and runtime-gradeable labs;
- two manual console drills.

Global automated regression therefore grows from 72 to 77 labs. The curriculum
catalog grows from 72 to 79 learning items.
