No `servera`, trabalhe em `/home/student/rhcsa-lab/obj05-05`.

Dois executáveis foram preparados:

```text
assets/nice-start
assets/nice-change
```

Tarefas:

1. Inicie `nice-start` em background com nice value **12**.
2. Grave o PID em `output/nice-start.pid`.
3. Inicie `nice-change` normalmente em background.
4. Grave o PID em `output/nice-change.pid`.
5. Use `renice` para alterar `nice-change` para nice value **7**.
6. Grave `ps -o pid=,ni=,stat=,args=` dos dois processos em
   `output/priorities.txt`.

Deixe os dois processos executando ao final.
