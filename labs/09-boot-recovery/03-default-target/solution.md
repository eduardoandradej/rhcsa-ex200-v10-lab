```bash
cd /home/student/rhcsa-lab/obj09-03
systemctl get-default
sudo systemctl set-default multi-user.target
systemctl get-default | tee output/default-target.txt
```
