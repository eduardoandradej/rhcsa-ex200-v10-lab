```bash
cd /home/student/rhcsa-lab/obj10-04
sudo setsebool -P httpd_enable_homedirs on
getsebool httpd_enable_homedirs > output/getsebool.txt
sudo semanage boolean -l | grep '^httpd_enable_homedirs ' > output/semanage.txt
sudo semanage boolean -l -C > output/custom.txt
```
