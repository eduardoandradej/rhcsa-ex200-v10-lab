```bash
sudo systemctl set-default multi-user.target
sudo grubby --update-kernel=ALL --args='systemd.show_status=1'

sudo mkdir -p /srv/boot12
echo 'tmpfs /srv/boot12 tmpfs rw,nosuid,nodev 0 0' |
  sudo tee -a /etc/fstab >/dev/null
sudo systemctl daemon-reload
sudo mount /srv/boot12

cd /home/student/rhcsa-lab/obj12-04
systemctl get-default > output/target.txt
sudo grubby --info=ALL > output/grubby.txt
findmnt /srv/boot12 > output/findmnt.txt
sudo findmnt --verify > output/verify.txt 2>&1
```
