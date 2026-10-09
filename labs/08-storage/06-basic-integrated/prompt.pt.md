Use **somente `/dev/vdb`**.

Crie uma GPT com:

- `vdb1`: aproximadamente 2 GiB, nome `basicdata`, XFS label `BASIC08`;
- `vdb2`: aproximadamente 1 GiB, nome `basicswap`, swap label `BASWAP08`.

Configure:

- `/dev/vdb1` montado persistentemente em `/basicdata` por **UUID**;
- `/dev/vdb2` ativo e persistente como swap por **UUID**;
- `/basicdata/marker.txt` contendo `OBJ08-BASIC`.

Execute `systemctl daemon-reload` e valide o fstab com `findmnt --verify`.

Salve `parted`, `lsblk -f`, `findmnt /basicdata` e `swapon --show` no diretório
`output/`.
