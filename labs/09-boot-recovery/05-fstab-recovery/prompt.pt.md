No `servera`, existe uma entrada de treinamento em `/etc/fstab` para um XFS em
`/dev/vdb1`, mas o estado foi preparado de forma incompleta.

1. Execute `sudo mount -a` e diagnostique a falha.
2. Descubra o UUID real de `/dev/vdb1`.
3. Corrija o ambiente para que o filesystem seja montado em
   `/srv/recovery09`.
4. A entrada final em `/etc/fstab` deve usar:
   `UUID=<uuid> /srv/recovery09 xfs defaults 0 0`.
5. Remova a opção de segurança `nofail` do estado final.
6. Execute `systemctl daemon-reload`.
7. Monte as entradas de `/etc/fstab`.
8. Valide com `findmnt --verify`.
9. Grave `findmnt /srv/recovery09` em `output/findmnt.txt` e a validação em
   `output/verify.txt`.

### Por que o setup usa `nofail`

O `nofail` existe **somente no estado inicial** para impedir que um reboot
acidental prenda a VM antes de você corrigir o exercício. O estado final
esperado não contém `nofail`.
