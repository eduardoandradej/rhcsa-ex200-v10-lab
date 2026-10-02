```bash
kill -s STOP "$(cat /run/rhcsa-signal-alpha.pid)"
kill -s TERM "$(cat /run/rhcsa-signal-beta.pid)"
kill -s CONT "$(cat /run/rhcsa-signal-gamma.pid)"
```
