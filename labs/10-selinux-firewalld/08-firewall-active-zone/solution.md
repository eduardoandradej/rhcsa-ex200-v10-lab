```bash
cd /home/student/rhcsa-lab/obj10-08

IFACE=$(ip -o route show default | awk '{print $5; exit}')
ZONE=$(sudo firewall-cmd --get-zone-of-interface="$IFACE")
if [ -z "$ZONE" ] || [ "$ZONE" = "no zone" ]; then
  ZONE=$(sudo firewall-cmd --get-default-zone)
fi

sudo firewall-cmd --permanent --zone="$ZONE" --add-port=45102/tcp
sudo firewall-cmd --reload

printf '%s\n' "$ZONE" > output/zone.txt
sudo firewall-cmd --zone="$ZONE" --query-port=45102/tcp > output/runtime.txt
sudo firewall-cmd --permanent --zone="$ZONE" --query-port=45102/tcp > output/permanent.txt
```
