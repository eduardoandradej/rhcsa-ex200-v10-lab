No `servera`, trabalhe em `/home/student/rhcsa-lab/obj04-06`.

O arquivo `assets/services.list` contém nomes, um por linha.

Crie `fileloop.sh`.

Requisitos:

1. Receba o arquivo como primeiro argumento.
2. Para cada item não vazio do arquivo, imprima:
   `ITEM:<valor>`
3. Preserve a ordem do arquivo.
4. Se o arquivo não existir:
   - `MISSING-FILE:<caminho>`
   - exit `1`
5. Sem argumento:
   - `Usage: fileloop.sh FILE` em stderr
   - exit `2`

O script deve funcionar com outros arquivos no mesmo formato.
