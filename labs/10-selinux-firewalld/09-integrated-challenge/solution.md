```bash
cd /home/student/rhcsa-lab/obj10-09

sudo semanage fcontext -a -t httpd_sys_content_t '/srv/rhcsa10-final(/.*)?'
sudo restorecon -Rv /srv/rhcsa10-final

sudo semanage port -a -t http_port_t -p tcp 48889

IFACE=$(ip -o route show default | awk '{print $5; exit}')
ZONE=$(sudo firewall-cmd --get-zone-of-interface="$IFACE")
if [ -z "$ZONE" ] || [ "$ZONE" = "no zone" ]; then
  ZONE=$(sudo firewall-cmd --get-default-zone)
fi

sudo firewall-cmd --permanent --zone="$ZONE" --add-port=48889/tcp
sudo firewall-cmd --reload
sudo systemctl start httpd

ls -Zd /srv/rhcsa10-final /srv/rhcsa10-final/index.html > output/contexts.txt
sudo semanage port -l -C | grep 48889 > output/selinux-port.txt
printf '%s\n' "$ZONE" > output/zone.txt
sudo firewall-cmd --zone="$ZONE" --query-port=48889/tcp > output/firewall.txt
curl -sS http://127.0.0.1:48889/secure10/index.html > output/curl.txt
```
