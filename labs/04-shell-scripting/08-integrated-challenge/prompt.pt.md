## Desafio integrado — Simple Shell Scripts

No `serverb`, trabalhe em `/home/student/rhcsa-lab/obj04-08`.

O arquivo `assets/users.list` contém nomes de usuários, um por linha.

Crie o script executável `account-audit.sh`.

### Interface

```text
./account-audit.sh INPUT_FILE OUTPUT_FILE
```

Se a quantidade de argumentos não for exatamente dois:

- escreva em stderr:
  `Usage: account-audit.sh INPUT_FILE OUTPUT_FILE`
- encerre com código `2`.

Se `INPUT_FILE` não existir:

- escreva:
  `MISSING-FILE:<caminho>`
- encerre com código `1`.

### Relatório

Para entrada válida, sobrescreva `OUTPUT_FILE` e gere:

```text
HOST=<hostname curto>
USER:<nome>:UID=<uid>:TYPE=<tipo>
...
SUMMARY:TOTAL=<total>:FOUND=<encontrados>:MISSING=<ausentes>
```

Classificação:

- UID `0` → `PRIVILEGED`
- UID entre `1` e `999` → `SYSTEM`
- UID `1000` ou maior → `REGULAR`
- usuário inexistente:
  `USER:<nome>:MISSING`

Requisitos:

- processe o arquivo em ordem;
- ignore linhas vazias;
- obtenha UID da base de usuários durante a execução;
- obtenha hostname durante a execução;
- calcule os totais dentro do script;
- para entrada válida, encerre com código `0`;
- o script deve funcionar com qualquer arquivo no mesmo formato.

O grader testará o script com uma segunda lista criada durante a avaliação.
