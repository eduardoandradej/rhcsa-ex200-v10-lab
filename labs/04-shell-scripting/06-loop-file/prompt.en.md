On `servera`, work in `/home/student/rhcsa-lab/obj04-06`.

File `assets/services.list` contains names, one per line.

Create `fileloop.sh`.

Requirements:

1. Receive the file as the first argument.
2. For each non-empty item in the file, print:
   `ITEM:<value>`
3. Preserve file order.
4. If the file does not exist:
   - `MISSING-FILE:<path>`
   - exit `1`
5. Without an argument:
   - `Usage: fileloop.sh FILE` to stderr
   - exit `2`

The script must work with other files in the same format.
