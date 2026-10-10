```bash
cd /home/student/rhcsa-lab/obj09-07

sudo systemctl set-default multi-user.target
sudo grubby --update-kernel=ALL --args="systemd.show_status=1"

sudo grubby --info=ALL > output/grubby.txt
systemctl get-default > output/default-target.txt
cat /proc/cmdline > output/current-cmdline.txt
sudo findmnt --verify | tee output/fstab-verify.txt
```
