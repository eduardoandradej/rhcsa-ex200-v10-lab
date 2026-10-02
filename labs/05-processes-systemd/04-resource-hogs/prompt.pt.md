No `servera`, o laboratório iniciou:

- `rhcsa-cpu-hog` — carga contínua de CPU;
- `rhcsa-mem-hog` — processo com alocação significativa de memória.

PIDs:

```text
/run/rhcsa-cpu-hog.pid
/run/rhcsa-mem-hog.pid
```

Trabalhe em `/home/student/rhcsa-lab/obj05-04`.

Antes de encerrar os processos:

1. Use `ps` ou `top` para investigar CPU e memória.
2. Salve a linha do processo de CPU em `output/cpu-before.txt`.
3. Salve a linha do processo de memória em `output/memory-before.txt`.
4. As linhas devem conter pelo menos PID, `%CPU`, `%MEM`, `STAT` e `ARGS`.

Depois, encerre os dois processos com `SIGTERM`.

Ao final, nenhum dos dois PIDs deve existir.
