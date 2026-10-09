O setup criou `/dev/vdb1`. No `servera`:

1. Formate `/dev/vdb1` como XFS com label `RHCSA08XFS`.
2. Monte-o temporariamente em `/mnt/rhcsa-xfs`.
3. Crie `/mnt/rhcsa-xfs/obj08.txt` contendo `OBJ08-XFS`.
4. Salve `findmnt /mnt/rhcsa-xfs` em `output/findmnt.txt`.
5. Salve `lsblk -f /dev/vdb` em `output/lsblk.txt`.

Não altere `/etc/fstab`.
