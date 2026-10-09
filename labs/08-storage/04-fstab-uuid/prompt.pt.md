O setup preparou `/dev/vdb1` como XFS e criou `/data1`.

1. Descubra o UUID de `/dev/vdb1`.
2. Adicione uma entrada em `/etc/fstab` usando **UUID**, montando em `/data1`
   como `xfs` com `defaults 0 0`.
3. Execute `systemctl daemon-reload`.
4. Monte usando apenas `mount /data1`.
5. Valide `/etc/fstab` com `findmnt --verify`.
6. Salve `findmnt /data1` em `output/findmnt.txt` e a saída da validação em
   `output/verify.txt`.

Não use `/dev/vdb1` no primeiro campo do fstab.
