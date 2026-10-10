Integrated challenge: set `multi-user.target` as default, add persistent
`systemd.show_status=1` to all kernel entries, verify `/etc/fstab`, and save
grubby/default-target/current-cmdline/fstab-verification evidence. Do not
reboot; the current `/proc/cmdline` is intentionally distinct from persistent
future boot configuration.
