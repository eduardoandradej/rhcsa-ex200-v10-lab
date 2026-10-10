Use only `/dev/vdb`. Create GPT storage with one partition, VG `vg12`,
an XFS LV `lvdata` of at least 1.4 GiB persistently mounted by UUID at
`/srv/data12`, plus an active persistent swap LV `lvswap` of at least
500 MiB. Save lsblk, LVM, mount, swap, and fstab verification evidence.
