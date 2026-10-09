No `servera`, faça um inventário **sem alterar o storage**.

Salve em `/home/student/rhcsa-lab/obj08-01/output/`:

- `lsblk.txt`: `lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,UUID`
- `blkid.txt`: saída de `sudo blkid`
- `parted-vdb.txt`: inspeção de `/dev/vdb` com `parted`
- `pvs.txt`, `vgs.txt`, `lvs.txt`: estado atual do LVM
- `findmnt.txt`: arquivos de sistema montados

Identifique mentalmente o disco do sistema e os quatro discos scratch. Não execute
`mklabel`, `mkfs`, `mkswap`, `pvcreate`, `wipefs` ou qualquer outro comando
destrutivo.
