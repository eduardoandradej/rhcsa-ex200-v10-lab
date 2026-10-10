```bash
cd /home/student/rhcsa-lab/obj11-03
echo '/- /etc/auto.rhcsa11' |
  sudo tee /etc/auto.master.d/rhcsa11.autofs
echo '/home/student/direct11 -fstype=nfs,rw,sync serverb:/srv/rhcsa11/direct' |
  sudo tee /etc/auto.rhcsa11
sudo systemctl enable --now autofs
cat /home/student/direct11/hello.txt > output/content.txt
findmnt -T /home/student/direct11/hello.txt > output/findmnt.txt
systemctl is-active autofs > output/service.txt
```
