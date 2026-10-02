```bash
cd /home/student/rhcsa-lab/obj03-01
rpm -q openssh-clients > output/package.txt
rpm -qf /usr/bin/ssh > output/owner.txt
rpm -qc openssh-clients > output/configs.txt
rpm -qd openssh-clients > output/docs.txt
rpm -ql openssh-clients > output/files.txt
```
