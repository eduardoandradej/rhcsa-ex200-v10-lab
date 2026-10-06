```bash
cd /home/student/rhcsa-lab/obj07-08
echo 'local5.notice /var/log/rhcsa-audit.log' | sudo tee /etc/rsyslog.d/rhcsa-audit.conf
sudo tee /etc/systemd/system/rhcsa-audit.service >/dev/null <<'EOF'
[Unit]
Description=RHCSA audit marker
[Service]
Type=oneshot
ExecStart=/usr/bin/logger -p local5.notice -t rhcsa-audit OBJ07-INTEGRATED-AUDIT
EOF
sudo tee /etc/systemd/system/rhcsa-audit.timer >/dev/null <<'EOF'
[Unit]
Description=RHCSA audit timer
[Timer]
OnBootSec=1min
OnUnitActiveSec=5min
Unit=rhcsa-audit.service
[Install]
WantedBy=timers.target
EOF
sudo rsyslogd -N1
sudo systemctl restart rsyslog
sudo systemctl daemon-reload
sudo systemctl enable --now rhcsa-audit.timer
sudo systemctl start rhcsa-audit.service
sudo journalctl --sync
sleep 1
systemctl status rhcsa-audit.timer --no-pager > output/timer.txt
sudo tail -n 20 /var/log/rhcsa-audit.log > output/syslog.txt
journalctl -t rhcsa-audit --since '-10 min' --no-pager > output/journal.txt
```
