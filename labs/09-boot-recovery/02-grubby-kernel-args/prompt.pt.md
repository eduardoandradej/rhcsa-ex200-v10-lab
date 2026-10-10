No `servera`, trabalhe em `/home/student/rhcsa-lab/obj09-02`.

1. Inspecione as entradas atuais com `grubby`.
2. Adicione o argumento persistente `systemd.show_status=1` a **todas** as
   entradas de kernel.
3. Confirme que o argumento aparece nas entradas persistentes.
4. Grave o resultado final de `grubby --info=ALL` em `output/grubby.txt`.

Não reinicie a máquina. Este exercício diferencia a configuração persistente
do boot atual: `/proc/cmdline` só mudaria após um novo boot.
