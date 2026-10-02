No `servera`, crie o script executável
`/home/student/rhcsa-lab/obj04-04/sysreport.sh`.

Sem argumentos, ele deve produzir **exatamente quatro linhas**, nesta ordem:

```text
HOSTNAME=<hostname curto>
KERNEL=<uname -r>
BASH_PATH=<caminho resolvido para bash>
USER_COUNT=<quantidade de entradas retornadas por getent passwd>
```

Os valores devem ser obtidos durante a execução do script a partir da saída dos comandos apropriados. Não grave valores fixos.
