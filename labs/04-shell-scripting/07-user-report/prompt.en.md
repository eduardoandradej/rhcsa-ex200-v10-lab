On `servera`, create executable script
`/home/student/rhcsa-lab/obj04-07/userreport.sh`.

It must process a variable number of user names supplied on the command line.

For each existing user, produce:

```text
USER:<name>:UID=<uid>:HOME=<home>:SHELL=<shell>
```

For a missing user:

```text
USER:<name>:MISSING
```

Additional requirements:

- preserve argument order;
- obtain system database information at run time;
- with zero arguments, print `NO-USERS` and exit `1`;
- with arguments, exit `0`, even if one user is missing.

Do not hardcode UID, home, or shell for known users.
