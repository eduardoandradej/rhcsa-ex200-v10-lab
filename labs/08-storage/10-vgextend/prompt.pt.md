O setup criou `rhcsa_vgextend` em `/dev/vdc1`.

Use **somente `/dev/vdd`** como segundo disco:

1. Crie GPT e `/dev/vdd1` com aproximadamente 2 GiB.
2. Marque a partição para LVM.
3. Crie o PV.
4. Adicione-o ao VG `rhcsa_vgextend`.
5. Crie o LV `rhcsa_lvextra` com 2 GiB.
6. Salve `pvs`, `vgs` e `lvs` em `output/`.
