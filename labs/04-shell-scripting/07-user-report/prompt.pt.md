No `servera`, crie o script executável
`/home/student/rhcsa-lab/obj04-07/userreport.sh`.

Ele deve processar uma quantidade variável de nomes de usuários recebidos pela linha de comando.

Para cada usuário existente, produza:

```text
USER:<nome>:UID=<uid>:HOME=<home>:SHELL=<shell>
```

Para usuário inexistente:

```text
USER:<nome>:MISSING
```

Requisitos adicionais:

- preserve a ordem dos argumentos;
- use informações obtidas da base do sistema durante a execução;
- com zero argumentos, imprima `NO-USERS` e encerre com código `1`;
- se houver argumentos, encerre com código `0`, mesmo que algum usuário não exista.

Não codifique UID, home ou shell de usuários conhecidos.
