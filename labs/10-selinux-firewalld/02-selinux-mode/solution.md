```bash
cd /home/student/rhcsa-lab/obj10-02
sudo setenforce 1
sudo sed -i 's/^SELINUX=.*/SELINUX=enforcing/' /etc/selinux/config
getenforce > output/getenforce.txt
grep '^SELINUX=' /etc/selinux/config > output/config.txt
```
