## Desafio integrado — Objective 01

No `servera`, como `student`, trabalhe em:

`/home/student/rhcsa-lab/obj01-10`

Não edite manualmente arquivos que o enunciado mandar produzir por comandos, filtros ou redirecionamentos.

1. Crie `work/{reports,logs,links,archive}`.
2. Copie `input/report.txt` para `work/reports/final-report.txt`, preservando o original.
3. A partir de `input/systems.txt`, selecione somente registros `prod` e `active` e grave em `work/reports/prod-active.txt`.
4. A partir de `input/events.log`, selecione linhas `WARN` ou `ERROR` com expressão regular estendida e grave em `work/logs/alerts.log`.
5. Grave em `work/reports/remote-host.txt` o FQDN do `serverb`, obtido por SSH a partir do `servera`.
6. Edite `work/reports/final-report.txt` para substituir `STATUS=PENDING` por `STATUS=READY`.
7. Ajuste `final-report.txt` para modo `0640` e o diretório `work/reports` para `0750`.
8. Crie um hard link `work/links/report.hard` para `work/reports/final-report.txt`.
9. Crie um symbolic link `work/links/alerts.current` apontando relativamente para `../logs/alerts.log`.
10. Crie `work/archive/evidence.tar.gz` contendo os diretórios `reports` e `logs` da árvore `work`.
11. Usando documentação local, grave apenas o caminho retornado por `man -w chmod` em `work/reports/chmod-manpath.txt`.

Ao terminar:

```bash
lab grade obj01-10
```
