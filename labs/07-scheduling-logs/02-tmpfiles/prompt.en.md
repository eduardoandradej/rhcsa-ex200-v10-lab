On `servera`, create `/etc/tmpfiles.d/rhcsa-momentary.conf` with:

```text
directory:   /run/rhcsa-momentary
mode:        0700
user:        root
group:       root
age:         30s
```

Use type `d`.

Then create `stale.txt`, leave it unused for more than 30 seconds, run
`systemd-tmpfiles --clean` using only this rule file, and save directory `stat`
output to `output/stat.txt`.

Final state: correct directory and `stale.txt` removed.
