No `servera`, o laboratório instalou `rhcsa-control.service`, inicialmente
inativo e desabilitado.

Trabalhe em `/home/student/rhcsa-lab/obj05-08`.

Tarefas:

1. Inicie `rhcsa-control.service`.
2. Grave o `MainPID` em `output/start.pid`.
3. Reinicie o serviço.
4. Grave o novo `MainPID` em `output/restart.pid`.
5. Execute `reload` no serviço.
6. Grave o `MainPID` após reload em `output/reload.pid`.
7. Deixe o serviço **ativo** ao final.

Resultado conceitual esperado:

- restart → PID muda;
- reload → PID principal não muda.

Não habilite o serviço para boot neste lab.
