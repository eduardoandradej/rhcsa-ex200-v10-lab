```bash
cd /home/student/rhcsa-lab/obj08-03
sudo mkfs.xfs -f -L RHCSA08XFS /dev/vdb1
sudo mount /dev/vdb1 /mnt/rhcsa-xfs
echo OBJ08-XFS | sudo tee /mnt/rhcsa-xfs/obj08.txt
findmnt /mnt/rhcsa-xfs > output/findmnt.txt
lsblk -f /dev/vdb > output/lsblk.txt
```
