O setup criou um LV XFS de 1 GiB montado em `/lvextend` com `keep.txt`.

1. Estenda `rhcsa_vgdata/rhcsa_lvdata` para **2 GiB de tamanho total**.
2. Expanda o XFS para usar o novo espaço, sem recriar o filesystem.
3. Preserve `/lvextend/keep.txt`.
4. Salve `lvs`, `df -h /lvextend` e `xfs_info /lvextend` em `output/`.
