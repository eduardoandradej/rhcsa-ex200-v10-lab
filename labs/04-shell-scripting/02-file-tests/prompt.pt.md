No `servera`, trabalhe em `/home/student/rhcsa-lab/obj04-02`.

Crie o script executável `checkpath.sh`, que recebe **um caminho** como primeiro argumento.

Comportamento:

- arquivo regular existente:
  `FILE:<caminho>` e exit `0`
- diretório existente:
  `DIRECTORY:<caminho>` e exit `0`
- caminho inexistente:
  `MISSING:<caminho>` e exit `1`
- nenhum argumento:
  `Usage: checkpath.sh PATH` em stderr e exit `2`

Use execução condicional de shell. Os caminhos de teste podem ser absolutos ou relativos.
