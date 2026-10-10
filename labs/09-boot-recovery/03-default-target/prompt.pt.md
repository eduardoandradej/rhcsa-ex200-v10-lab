No `servera`, configure `multi-user.target` como o target padrão do systemd.

1. Consulte o target padrão atual.
2. Altere o target padrão para `multi-user.target`.
3. Confirme a alteração.
4. Grave a saída de `systemctl get-default` em
   `/home/student/rhcsa-lab/obj09-03/output/default-target.txt`.

Não use `systemctl isolate` neste exercício e não reinicie a VM.
