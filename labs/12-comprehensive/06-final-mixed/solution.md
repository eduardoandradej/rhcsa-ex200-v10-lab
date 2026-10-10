```bash
sudo groupadd opsfinal12
sudo useradd -m -s /bin/bash -G opsfinal12 operator12

sudo mkdir -p /srv/final12
sudo chown root:opsfinal12 /srv/final12
sudo chmod 2770 /srv/final12

echo '/remote12-final /etc/auto.final12' |
  sudo tee /etc/auto.master.d/final12.autofs >/dev/null
echo '* -rw,sync,fstype=nfs serverb:/srv/rhcsa11/integrated/&' |
  sudo tee /etc/auto.final12 >/dev/null
sudo systemctl enable --now autofs

sudo tee /usr/local/bin/final-report12 >/dev/null <<'EOF'
#!/bin/bash
set -Eeuo pipefail
[[ $# -eq 1 ]] || exit 2
key="$1"
case "$key" in
  red|hat) ;;
  *) exit 2 ;;
esac
cat "/remote12-final/$key/info.txt" > "/srv/final12/report-$key.txt"
EOF
sudo chmod 0755 /usr/local/bin/final-report12

sudo -u operator12 /usr/local/bin/final-report12 red
sudo -u operator12 /usr/local/bin/final-report12 hat

echo '*/15 * * * * operator12 /usr/local/bin/final-report12 red' |
  sudo tee /etc/cron.d/final12 >/dev/null
sudo chmod 0644 /etc/cron.d/final12

cd /home/student/rhcsa-lab/obj12-06
id operator12 > output/id.txt
{
  findmnt -T /remote12-final/red/info.txt
  findmnt -T /remote12-final/hat/info.txt
} > output/mounts.txt
{
  sudo cat /srv/final12/report-red.txt
  sudo cat /srv/final12/report-hat.txt
} > output/reports.txt
cat /etc/cron.d/final12 > output/cron.txt
```
