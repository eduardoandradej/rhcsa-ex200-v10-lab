Manual console drill. Reboot `servera`, temporarily append
`systemd.unit=emergency.target` in the GRUB editor, inspect the root mount,
remount it read/write only if needed, compare emergency and rescue behavior,
then return to normal boot. This drill is intentionally excluded from the
automated harness because the bastion has no privileged libvirt host-control
channel.
