On `servera`, create `/home/student/rhcsa-lab/obj04-03/checkcmd.sh`.

The script receives **one command name**.

Requirements:

- if the command exists in `PATH`:
  `FOUND:<command>:<resolved-path>` and exit `0`
- if it does not exist:
  `NOTFOUND:<command>` and exit `1`
- without an argument:
  `Usage: checkcmd.sh COMMAND` to stderr and exit `2`

Resolve the path from the system; do not hardcode command paths.
