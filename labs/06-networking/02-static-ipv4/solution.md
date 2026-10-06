```bash
cd /home/student/rhcsa-lab/obj06-02
sudo nmcli con add con-name ex200-static type ethernet ifname ex200a \
  ipv4.method manual ipv4.addresses 10.66.2.10/24 \
  ipv6.method disabled connection.autoconnect yes
sudo nmcli con up ex200-static
ping -c 2 10.66.2.254 > output/ping.txt
```