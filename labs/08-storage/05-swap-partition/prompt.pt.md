O setup criou `/dev/vde1`.

1. Inicialize `/dev/vde1` como swap com label `RHCSA08SWAP`.
2. Ative o swap.
3. Adicione-o ao `/etc/fstab` usando UUID com `none swap defaults 0 0`.
4. Execute `systemctl daemon-reload`.
5. Salve `swapon --show` em `output/swapon.txt`.
6. Salve `free -h` em `output/free.txt`.
7. Valide o fstab com `findmnt --verify`.

Não altere o swap original do sistema.
