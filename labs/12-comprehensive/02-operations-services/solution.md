```bash
sudo sh -c 'printf "%s\n" "OBJ12 operations ready" > /var/www/html/ops12.html'
sudo systemctl enable --now httpd

echo '*/10 * * * * student /usr/bin/date >> /home/student/ops12-cron.log' |
  sudo tee /etc/cron.d/ops12 >/dev/null
sudo chmod 0644 /etc/cron.d/ops12

echo 'd /run/ops12 0750 student student -' |
  sudo tee /etc/tmpfiles.d/ops12.conf >/dev/null
sudo systemd-tmpfiles --create /etc/tmpfiles.d/ops12.conf

echo 'local6.* /var/log/ops12.log' |
  sudo tee /etc/rsyslog.d/ops12.conf >/dev/null
sudo systemctl restart rsyslog
logger -p local6.notice -t obj12 'OBJ12 operations ready'
sleep 1

cd /home/student/rhcsa-lab/obj12-02
curl -sS http://127.0.0.1/ops12.html > output/curl.txt
{
  systemctl is-active httpd
  systemctl is-enabled httpd
} > output/httpd.txt
cat /etc/cron.d/ops12 > output/cron.txt
stat -c '%a %U %G %n' /run/ops12 > output/tmpfiles.txt
sudo grep 'OBJ12 operations ready' /var/log/ops12.log | tail -1 > output/log.txt
```
