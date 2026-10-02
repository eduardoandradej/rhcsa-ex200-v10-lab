## Integrated challenge — Users & Groups

On `serverb`, as `student`, use administrative privileges to reach this state:

1. Set `PASS_MAX_DAYS` to `30` in `/etc/login.defs`.
2. Create group `consultantsx` with GID `35050`.
3. Create `/etc/sudoers.d/consultantsx`, mode `0440`, allowing members of `consultantsx` to run any command as any user.
4. Create `consultx1`, `consultx2`, and `consultx3` with `consultantsx` as a supplementary group.
5. Set the lab password `redhat` for all three accounts.
6. Make all three accounts expire 90 days from today.
7. For `consultx2`, configure a 15-day maximum password age.
8. Force all three accounts to change their passwords at the next login.
9. Validate the sudoers file with `visudo`.

`lab finish` restores `/etc/login.defs` to its pre-lab state.
