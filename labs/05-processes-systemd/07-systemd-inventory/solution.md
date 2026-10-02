```bash
cd /home/student/rhcsa-lab/obj05-07

systemctl list-units --type=service --all --no-pager > output/services.txt
systemctl list-unit-files --type=service --no-pager > output/unit-files.txt
systemctl is-active sshd.service > output/sshd-active.txt
systemctl is-enabled sshd.service > output/sshd-enabled.txt
systemctl status chronyd.service --no-pager > output/chronyd-status.txt
```
