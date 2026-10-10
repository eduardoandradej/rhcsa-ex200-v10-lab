Manual-only superuser recovery drill. Practice interrupting GRUB, entering a
recovery environment, remounting the root filesystem read/write, resetting the
root password, arranging SELinux relabeling, and returning to normal boot.

The local serial-console harness does not automate this task because the RHEL
10 no-media recovery path can require console-argument changes that may remove
the very serial channel used by `virsh console`.
