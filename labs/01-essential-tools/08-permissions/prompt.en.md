On `servera`, as `student`, work in:

`/home/student/rhcsa-lab/obj01-08`

1. Set `data/report.txt` so that the owner has read/write, the group has read only, and others have no access.
2. Set `data/scripts` to `rwx` for the owner, `rx` for the group, and no access for others.
3. On `data/scripts/backup.sh`, add execute permission only for the owner while preserving the other existing permissions.
4. In the current shell, set `umask 0027`.
5. With that `umask`, create `generated/new-file.txt` and `generated/new-dir`.
6. Do not manually change the permissions of the two objects created in the previous step; their modes must result from the `umask`.

When finished, return to bastion and run `lab grade obj01-08`.
