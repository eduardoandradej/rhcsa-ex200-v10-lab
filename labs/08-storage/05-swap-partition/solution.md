```bash
cd /home/student/rhcsa-lab/obj08-05
sudo mkswap -L RHCSA08SWAP /dev/vde1
sudo swapon /dev/vde1
UUID=$(sudo blkid -s UUID -o value /dev/vde1)
echo "UUID=$UUID none swap defaults 0 0" | sudo tee -a /etc/fstab
sudo systemctl daemon-reload
swapon --show > output/swapon.txt
free -h > output/free.txt
findmnt --verify
```
