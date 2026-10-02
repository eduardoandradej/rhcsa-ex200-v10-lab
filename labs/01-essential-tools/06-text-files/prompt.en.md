On `servera`, as `student`, edit the following file with `vim`:

`/home/student/rhcsa-lab/obj01-06/app.conf`

Make these changes:

1. Change `environment=development` to `environment=production`.
2. Change `workers=2` to `workers=8`.
3. Completely remove the `debug=true` line.
4. Add `logging=verbose` immediately after `workers=8`.
5. Preserve the first comment line and the `port=8080` line.
6. Also create `notes.txt` with exactly these three lines:

```text
review completed
configuration updated
ready for validation
```

Do not replace the file with a prebuilt copy; practice interactive terminal editing.
