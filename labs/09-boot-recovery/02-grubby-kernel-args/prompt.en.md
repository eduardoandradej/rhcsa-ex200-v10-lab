On `servera`, add persistent kernel argument `systemd.show_status=1` to all
kernel entries with `grubby`. Save final `grubby --info=ALL` output to
`output/grubby.txt`. Do not reboot.
