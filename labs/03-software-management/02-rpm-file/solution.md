```bash
cd /home/student/rhcsa-lab/obj03-02
rpm -qpi rhcsa-inspect-1.0-1.noarch.rpm > output/info.txt
rpm -qpl rhcsa-inspect-1.0-1.noarch.rpm > output/files.txt
rpm -qpc rhcsa-inspect-1.0-1.noarch.rpm > output/configs.txt
rpm -qp --scripts rhcsa-inspect-1.0-1.noarch.rpm > output/scripts.txt
cd extracted
rpm2cpio ../rhcsa-inspect-1.0-1.noarch.rpm | cpio -id
```
