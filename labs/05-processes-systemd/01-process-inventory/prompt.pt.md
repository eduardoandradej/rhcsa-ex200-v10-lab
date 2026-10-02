No `servera`, o `lab start` criou dois processos de treinamento:

- `rhcsa-proc-sleeper`
- `rhcsa-proc-stopped`

Os respectivos PIDs estão em:

```text
/run/rhcsa-proc-sleeper.pid
/run/rhcsa-proc-stopped.pid
```

Trabalhe em `/home/student/rhcsa-lab/obj05-01`.

Gere, usando `ps`, exatamente estes dois relatórios:

```text
output/sleeper.txt
output/stopped.txt
```

Cada relatório deve usar estas colunas, sem cabeçalho:

```text
PID PPID STAT NI ARGS
```

Use o PID correspondente a cada processo.

Objetivo: identificar PID, PPID, estado (`STAT`), nice value e linha de comando. Não altere nem finalize os processos.
