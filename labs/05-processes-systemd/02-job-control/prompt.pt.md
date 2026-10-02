No `servera`, trabalhe em `/home/student/rhcsa-lab/obj05-02`.

Use **uma única sessão Bash** para realizar o exercício.

Os executáveis já existem:

```text
assets/job-alpha
assets/job-beta
```

Tarefas:

1. Inicie `job-alpha` em background e grave `$!` em `output/alpha.pid`.
2. Inicie `job-beta` em background e grave `$!` em `output/beta.pid`.
3. Use controle de jobs para suspender `job-alpha`.
4. Deixe `job-beta` executando em background.
5. Grave `jobs -l` em `output/jobs.txt`.
6. Grave em `output/processes.txt` o `ps` dos dois PIDs com:
   `pid,stat,args`, sem cabeçalho.

Estado final:

- `job-alpha`: parado (`T`);
- `job-beta`: executando/dormindo, mas não parado.

Não finalize os dois processos; o `lab finish` fará a limpeza.
