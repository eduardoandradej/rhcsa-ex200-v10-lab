Configure an on-demand NFS mount through `/etc/fstab` and
`x-systemd.automount`, not AutoFS. Use `rw,sync,x-systemd.automount`, reload
systemd, start the generated automount unit, access the file to trigger the
mount, and save unit, findmnt, and content evidence.
