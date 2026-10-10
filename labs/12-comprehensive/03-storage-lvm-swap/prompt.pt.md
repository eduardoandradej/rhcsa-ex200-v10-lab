## Cenário

Use **somente `/dev/vdb`** como disco de treinamento. O disco do sistema não
deve ser alterado.

Entregue o seguinte estado:

- tabela GPT em `/dev/vdb`;
- uma partição `/dev/vdb1` com pelo menos 3 GiB;
- `/dev/vdb1` como PV do VG `vg12`;
- LV `lvdata` com pelo menos 1,4 GiB;
- `lvdata` formatado XFS, label `DATA12`, montado persistentemente em
  `/srv/data12` por UUID;
- LV `lvswap` com pelo menos 500 MiB;
- `lvswap` formatado como swap, label `SWAP12`, ativo e persistente por UUID;
- `/etc/fstab` válido.

Grave em `output/`:

- `lsblk.txt`: `lsblk -f /dev/vdb`;
- `lvm.txt`: saída de `pvs`, `vgs` e `lvs` para o ambiente criado;
- `findmnt.txt`: montagem de `/srv/data12`;
- `swap.txt`: estado ativo de swap;
- `verify.txt`: validação do `fstab`.
