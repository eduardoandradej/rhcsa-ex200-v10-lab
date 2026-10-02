## Desafio integrado — Processos, prioridade, TuneD e systemd

No `serverb`, trabalhe em `/home/student/rhcsa-lab/obj05-10`.

O ambiente contém:

- processo intensivo `rhcsa-rogue-cpu`, já em execução;
- executável `assets/batch-worker`;
- `rhcsa-api.service`, inicialmente inativo/desabilitado;
- `rhcsa-legacy.service`, inicialmente ativo/habilitado;
- TuneD preparado para alteração de perfil.

### Tarefas

1. Identifique o processo `rhcsa-rogue-cpu`.
2. Antes de finalizá-lo, grave:
   `ps -o pid=,%cpu=,%mem=,ni=,stat=,args=`
   em `output/rogue-before.txt`.
3. Finalize `rhcsa-rogue-cpu` com `SIGTERM`.
4. Inicie `assets/batch-worker` em background com nice value **10**.
5. Grave `$!` em `output/batch.pid`.
6. Deixe `rhcsa-api.service` **ativo e habilitado**.
7. Deixe `rhcsa-legacy.service` **inativo e mascarado**.
8. Ative o perfil TuneD `balanced`.
9. Grave `tuned-adm active` em `output/tuned-active.txt`.

### Estado final obrigatório

```text
rhcsa-rogue-cpu       ausente
batch-worker          executando com NI=10
rhcsa-api.service     active + enabled
rhcsa-legacy.service  inactive + masked
TuneD                 balanced
```

O grader usa PIDs e estado atual do sistema; não codifique resultados.
