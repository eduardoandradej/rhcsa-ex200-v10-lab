```bash
cd /home/student/rhcsa-lab/obj05-09

sudo systemctl enable --now rhcsa-boot.service
systemctl list-dependencies rhcsa-boot.service --no-pager \
  > output/boot-dependencies.txt

sudo systemctl stop rhcsa-blocked.service
sudo systemctl disable rhcsa-blocked.service
sudo systemctl mask rhcsa-blocked.service
```
