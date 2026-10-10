A training XFS filesystem has an incomplete `/etc/fstab` configuration.
Diagnose `mount -a`, create/fix `/srv/recovery09`, leave a final UUID-based
`defaults 0 0` entry without `nofail`, reload systemd, mount it, validate the
fstab, and save `findmnt` and verification output.
