# Objective 07 — Scheduling, Temporary Files, Logging & Time

Eight labs cover systemd timers, systemd-tmpfiles, `/etc/cron.d`, rsyslog routing, journalctl filters, persistent journald storage, timezone/Chrony, and an integrated scheduling/logging challenge.

RHEL 10 emphasizes systemd timer units for most recurring system tasks while cron remains relevant for recurring jobs. Administrator overrides stay under `/etc`; vendor files under `/usr/lib` are not edited directly.
