```bash
cd /home/student/rhcsa-lab/obj08-04
UUID=$(sudo blkid -s UUID -o value /dev/vdb1)
echo "UUID=$UUID /data1 xfs defaults 0 0" | sudo tee -a /etc/fstab
sudo systemctl daemon-reload
sudo mount /data1
findmnt --verify | tee output/verify.txt
findmnt /data1 > output/findmnt.txt
```
