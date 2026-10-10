```bash
cd /home/student/rhcsa-lab/obj11-02
echo 'serverb:/srv/rhcsa11/persist /mnt/rhcsa11-persist nfs rw,sync 0 0' |
  sudo tee -a /etc/fstab
sudo systemctl daemon-reload
sudo mount /mnt/rhcsa11-persist
findmnt /mnt/rhcsa11-persist > output/findmnt.txt
sudo findmnt --verify > output/verify.txt 2>&1
cat /mnt/rhcsa11-persist/hello.txt > output/content.txt
```
