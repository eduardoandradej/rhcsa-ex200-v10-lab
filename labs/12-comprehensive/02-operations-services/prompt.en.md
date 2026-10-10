Deliver an operational server state with enabled/running httpd, a fixed web
page, a cron entry every ten minutes as student, a tmpfiles rule creating
`/run/ops12` as `student:student` mode 0750, and rsyslog routing `local6.*`
to `/var/log/ops12.log`. Save evidence under `output/`.
