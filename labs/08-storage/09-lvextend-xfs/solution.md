```bash
cd /home/student/rhcsa-lab/obj08-09
sudo lvextend -L 2G /dev/rhcsa_vgdata/rhcsa_lvdata
sudo xfs_growfs /lvextend
sudo lvs > output/lvs.txt
df -h /lvextend > output/df.txt
sudo xfs_info /lvextend > output/xfs-info.txt
```
