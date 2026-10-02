# Hotfix 0.8.2 — obj02-04 grader privilege boundary

## Causa

O estado produzido pelo solver estava correto. O erro ocorria no próprio
grader.

`/home/teamuser1` possui as permissões privadas normais de um diretório home.
O checker remoto é executado como `student`; portanto, tentar usar
`Path.stat()` diretamente em:

`/home/teamuser1/projecta-owned.txt`

pode gerar `PermissionError` antes que o grader retorne JSON.

## Correção

O grader continua sendo executado como `student`, mas usa `sudo -n` somente
para inspecionar o arquivo que pertence a outro usuário:

- `test -f` valida que é um arquivo regular;
- `stat -c %U:%G` valida proprietário e grupo.

Isso mantém a avaliação por estado final sem relaxar as permissões do home.

## Validação

Primeiro reteste somente o ponto que falhou:

```bash
bash tests/integration-reference.sh obj02-04
```

Se passar:

```bash
bash tests/integration-reference.sh   obj02-05 obj02-06 obj02-07 obj02-08
```

Não há necessidade de repetir `obj02-01` a `obj02-03`.
