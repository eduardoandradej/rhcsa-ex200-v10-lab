On `servera`:

1. Add `svcadmin` to supplementary group `opsadmin`.
2. Create `/etc/sudoers.d/opsadmin` with mode `0440`.
3. Allow members of `opsadmin` to run, as `root` and without a password, only:
   - `/usr/bin/id`
   - `/usr/bin/whoami`
4. Validate the configuration syntax with `visudo`.
5. Confirm that `svcadmin` can run `sudo /usr/bin/id -u`.

Do not directly modify `/etc/sudoers`.
