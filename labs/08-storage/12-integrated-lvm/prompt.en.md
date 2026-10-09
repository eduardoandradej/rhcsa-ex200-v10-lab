Integrated challenge using only /dev/vdc and /dev/vdd: create two LVM PVs,
VG rhcsa_vgfinal, 2GiB data LV and 512MiB swap LV; persist XFS data at
/lvfinal and swap by UUID; then grow data LV/XFS to 3GiB preserving marker.
