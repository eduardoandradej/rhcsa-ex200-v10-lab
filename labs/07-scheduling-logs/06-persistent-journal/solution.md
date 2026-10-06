```bash
cd /home/student/rhcsa-lab/obj07-06
sudo mkdir -p /etc/systemd/journald.conf.d
sudo tee /etc/systemd/journald.conf.d/99-rhcsa-persistent.conf >/dev/null <<'EOF'
[Journal]
Storage=persistent
SystemMaxUse=100M
EOF
sudo mkdir -p /var/log/journal
sudo systemctl restart systemd-journald
sudo journalctl --flush
journalctl --list-boots --no-pager > output/boots.txt
journalctl --disk-usage > output/disk-usage.txt
```
