## Integrated challenge — Simple Shell Scripts

On `serverb`, work in `/home/student/rhcsa-lab/obj04-08`.

File `assets/users.list` contains user names, one per line.

Create executable script `account-audit.sh`.

### Interface

```text
./account-audit.sh INPUT_FILE OUTPUT_FILE
```

If the argument count is not exactly two:

- write to stderr:
  `Usage: account-audit.sh INPUT_FILE OUTPUT_FILE`
- exit with code `2`.

If `INPUT_FILE` does not exist:

- write:
  `MISSING-FILE:<path>`
- exit with code `1`.

### Report

For valid input, overwrite `OUTPUT_FILE` and generate:

```text
HOST=<short hostname>
USER:<name>:UID=<uid>:TYPE=<type>
...
SUMMARY:TOTAL=<total>:FOUND=<found>:MISSING=<missing>
```

Classification:

- UID `0` → `PRIVILEGED`
- UID `1` through `999` → `SYSTEM`
- UID `1000` or greater → `REGULAR`
- missing user:
  `USER:<name>:MISSING`

Requirements:

- process the file in order;
- ignore blank lines;
- obtain UID from the user database at run time;
- obtain hostname at run time;
- calculate totals inside the script;
- for valid input, exit `0`;
- the script must work with any file in the same format.

The grader will test the script with a second list created during evaluation.
