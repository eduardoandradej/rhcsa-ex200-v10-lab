```bash
cd /home/student/rhcsa-lab/obj09-05

sudo mount -a

UUID=$(sudo blkid -s UUID -o value /dev/vdb1)
sudo mkdir -p /srv/recovery09

sudo sed -i '\|[[:space:]]/srv/recovery09[[:space:]]|d' /etc/fstab
echo "UUID=$UUID /srv/recovery09 xfs defaults 0 0" | sudo tee -a /etc/fstab

sudo systemctl daemon-reload
sudo mount -a

sudo findmnt --verify | tee output/verify.txt
findmnt /srv/recovery09 > output/findmnt.txt
```
