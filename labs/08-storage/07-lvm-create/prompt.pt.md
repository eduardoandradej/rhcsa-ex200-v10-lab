Use **somente `/dev/vdc`**.

1. Crie GPT.
2. Crie `/dev/vdc1` de aproximadamente 4 GiB e marque-o para LVM.
3. Crie o PV em `/dev/vdc1`.
4. Crie o VG `rhcsa_vgdata`.
5. Crie o LV `rhcsa_lvdata` com 1536 MiB.
6. Salve `pvs`, `vgs` e `lvs` em `output/`.

Não crie filesystem neste lab.
