```bash
sudo semanage fcontext -a -t httpd_sys_content_t '/srv/secure12(/.*)?'
sudo restorecon -Rv /srv/secure12
sudo semanage port -a -t http_port_t -p tcp 48890

IFACE=$(ip -o route show default | awk '{print $5; exit}')
ZONE=$(sudo firewall-cmd --get-zone-of-interface="$IFACE")
if [ -z "$ZONE" ] || [ "$ZONE" = "no zone" ]; then
  ZONE=$(sudo firewall-cmd --get-default-zone)
fi
sudo firewall-cmd --permanent --zone="$ZONE" --add-port=48890/tcp
sudo firewall-cmd --reload
sudo systemctl enable --now httpd

cd /home/student/rhcsa-lab/obj12-05
ls -Zd /srv/secure12 /srv/secure12/index.html > output/contexts.txt
sudo semanage port -l -C | grep 48890 > output/selinux-port.txt
sudo firewall-cmd --zone="$ZONE" --query-port=48890/tcp > output/firewall.txt
{
  systemctl is-active httpd
  systemctl is-enabled httpd
} > output/service.txt
curl -sS http://127.0.0.1:48890/secure12/index.html > output/curl.txt
```
