Use **somente `/dev/vde`**.

1. Crie GPT e uma partição LVM com aproximadamente 1536 MiB.
2. Crie o PV e o VG `rhcsa_vgswap`.
3. Crie o LV `rhcsa_lvswap` com 768 MiB.
4. Inicialize-o como swap com label `LVSWAP08`.
5. Ative-o.
6. Persista no fstab por **UUID**.
7. Salve `pvs`, `vgs`, `lvs` e `swapon --show` em `output/`.

Preserve o swap original do sistema.
