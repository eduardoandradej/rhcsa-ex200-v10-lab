## Desafio integrado — boot, kernel e systemd

No `servera`, trabalhe em `/home/student/rhcsa-lab/obj09-07`.

Deixe o sistema no seguinte estado:

1. `multi-user.target` deve ser o target padrão.
2. Todas as entradas de kernel devem possuir o argumento persistente
   `systemd.show_status=1`.
3. `/etc/fstab` deve passar em `findmnt --verify`.
4. Grave:
   - `grubby --info=ALL` em `output/grubby.txt`;
   - `systemctl get-default` em `output/default-target.txt`;
   - `/proc/cmdline` em `output/current-cmdline.txt`;
   - a validação do fstab em `output/fstab-verify.txt`.

Não reinicie o sistema.

Atenção: o novo argumento foi persistido no boot loader, mas
`/proc/cmdline` representa **o boot atual**. Portanto, não espere que o novo
argumento apareça em `/proc/cmdline` antes de um reboot.
