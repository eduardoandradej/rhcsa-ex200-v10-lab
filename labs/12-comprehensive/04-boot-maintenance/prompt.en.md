Without rebooting, set the default target to `multi-user.target`, persist
`systemd.show_status=1` in all grubby-managed kernel entries, and create a
persistent active tmpfs mount at `/srv/boot12` with `rw,nosuid,nodev`.
Save target, grubby, mount, and fstab verification evidence.
