## Cenário

Ajuste o estado persistente do `servera` sem reiniciar a máquina:

- target padrão: `multi-user.target`;
- argumento `systemd.show_status=1` presente persistentemente em todas as
  entradas de kernel gerenciadas pelo `grubby`;
- `/srv/boot12` como mount point de um `tmpfs`;
- `/etc/fstab` deve conter uma entrada persistente para `/srv/boot12`, tipo
  `tmpfs`, com as opções `rw,nosuid,nodev`;
- a montagem deve estar ativa;
- o `fstab` deve passar na validação.

Grave em `output/`:

- `target.txt`;
- `grubby.txt`;
- `findmnt.txt`;
- `verify.txt`.

Não reinicie o servidor.
