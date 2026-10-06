```bash
cd /home/student/rhcsa-lab/obj06-07
sudo nmcli con mod ex200-dns \
  ipv4.dns "192.0.2.53 192.0.2.54" ipv4.dns-search lab.example \
  ipv4.ignore-auto-dns yes ipv4.never-default yes connection.autoconnect no
nmcli -f ipv4.dns,ipv4.dns-search,ipv4.ignore-auto-dns,ipv4.never-default,connection.autoconnect con show ex200-dns > output/dns-profile.txt
grep '^hosts:' /etc/nsswitch.conf > output/nsswitch-hosts.txt
```