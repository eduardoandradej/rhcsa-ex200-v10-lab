Start on `servera` as `student`.

Exercise directory:

`/home/student/rhcsa-lab/obj01-04`

1. From `servera`, access `student@serverb` through SSH and save the remote FQDN in `remote-host.txt`.
2. From `servera`, access `student@serverb` again and save the remote user name in `remote-user.txt`.
3. On `servera`, switch to the `labuser` account by using a login shell. The lab password for this account is `redhat`.
4. As `labuser`, create `/home/labuser/switch-user.txt` containing only the output of `whoami`.
5. Exit the `labuser` session and return to `student`.

The goal is to practice SSH access and actual user identity switching; do not manually type the expected values into the result files.
