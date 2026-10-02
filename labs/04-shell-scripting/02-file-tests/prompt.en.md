On `servera`, work in `/home/student/rhcsa-lab/obj04-02`.

Create executable script `checkpath.sh`, which receives **one path** as its first argument.

Behavior:

- existing regular file:
  `FILE:<path>` and exit `0`
- existing directory:
  `DIRECTORY:<path>` and exit `0`
- missing path:
  `MISSING:<path>` and exit `1`
- no argument:
  `Usage: checkpath.sh PATH` to stderr and exit `2`

Use shell conditional execution. Test paths may be absolute or relative.
