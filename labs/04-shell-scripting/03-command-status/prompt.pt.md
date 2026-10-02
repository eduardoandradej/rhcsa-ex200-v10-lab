No `servera`, crie `/home/student/rhcsa-lab/obj04-03/checkcmd.sh`.

O script recebe **um nome de comando**.

Requisitos:

- se o comando existir no `PATH`:
  `FOUND:<comando>:<caminho-resolvido>` e exit `0`
- se não existir:
  `NOTFOUND:<comando>` e exit `1`
- sem argumento:
  `Usage: checkcmd.sh COMMAND` em stderr e exit `2`

O caminho deve ser obtido pelo próprio sistema; não codifique caminhos de comandos manualmente.
