O setup criou `/dev/rhcsa_vgdata/rhcsa_lvdata`.

1. Formate o LV como XFS com label `LVDATA08`.
2. Monte persistentemente em `/lvdata` usando **UUID** no fstab.
3. Crie `/lvdata/marker.txt` contendo `OBJ08-LVDATA`.
4. Valide o fstab.
5. Salve `findmnt /lvdata`, `lsblk -f` e `lvs` em `output/`.
