No `servera`, trabalhe em `/home/student/rhcsa-lab/obj09-01`.

Sem alterar a configuração do sistema:

1. Grave a versão do kernel em `output/kernel.txt`.
2. Grave a linha de comando do kernel atual em `output/cmdline.txt`.
3. Identifique o kernel padrão do boot loader e grave-o em
   `output/default-kernel.txt`.
4. Grave todas as entradas conhecidas pelo `grubby` em `output/grubby.txt`.
5. Identifique o target padrão do systemd e grave-o em
   `output/default-target.txt`.

O objetivo é diferenciar **kernel em execução**, **kernel configurado como
padrão**, **argumentos do boot atual** e **target padrão do systemd**.
