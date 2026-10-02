# Hotfix 0.7.2 — nested SSH stdin safety

Causa:

Os reference solvers são enviados para `servera` por stdin:

```bash
ssh servera 'bash -s' <<'EOS'
...
EOS
```

Dentro desse script havia outro comando `ssh`. Por padrão, esse SSH interno
também lê stdin e podia consumir o restante do heredoc. Por isso somente o
primeiro comando remoto era executado, enquanto as linhas seguintes nunca
chegavam ao `bash`.

Correção:

```bash
ssh -n -o BatchMode=yes ...
```

O `-n` redireciona o stdin do SSH interno para `/dev/null`.

Arquivos corrigidos:

- `tests/reference-solutions/obj01-04.sh`
- `tests/reference-solutions/obj01-10.sh`

Validação:

```bash
bash tests/integration-reference.sh obj01-04 obj01-10
```
