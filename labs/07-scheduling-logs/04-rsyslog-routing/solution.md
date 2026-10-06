```bash
cd /home/student/rhcsa-lab/obj07-04
echo 'local6.debug /var/log/rhcsa-debug.log' | sudo tee /etc/rsyslog.d/rhcsa-debug.conf
sudo rsyslogd -N1
sudo systemctl restart rsyslog
logger -p local6.debug -t obj07-rsyslog 'OBJ07-RSYSLOG-DEBUG'
sleep 1
sudo tail -n 20 /var/log/rhcsa-debug.log > output/log.txt
```
