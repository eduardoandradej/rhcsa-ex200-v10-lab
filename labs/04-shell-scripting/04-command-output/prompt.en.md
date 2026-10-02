On `servera`, create executable script
`/home/student/rhcsa-lab/obj04-04/sysreport.sh`.

With no arguments, it must produce **exactly four lines**, in this order:

```text
HOSTNAME=<short hostname>
KERNEL=<uname -r>
BASH_PATH=<resolved path for bash>
USER_COUNT=<number of entries returned by getent passwd>
```

Values must be obtained at script run time from command output. Do not hardcode them.
