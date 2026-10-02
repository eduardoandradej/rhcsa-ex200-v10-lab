On `servera`, working as `student`, use:

`/home/student/rhcsa-lab/obj01-03`

Use `grep` and regular expressions to produce the files below. Do not manually edit the results.

1. From `input/systems.txt`, select only lines whose first field is `SRV-` followed by exactly three digits. Save them to `output/servers.txt`.
2. Select every line whose hostname begins with `web`. Save them to `output/web-hosts.txt`.
3. Select only systems that are both in the `prod` environment and have the `active` state. Save them to `output/prod-active.txt`.
4. From `input/events.log`, select lines containing `WARN` or `ERROR` by using an extended regular expression. Save them to `output/alerts.log`.
5. From `input/systems.txt`, select lines whose IP address ends in `.21`. Save them to `output/ip-ending-21.txt`.

Preserve the original line order.

When finished, return to the bastion and run `lab grade obj01-03`.
