No `servera`, como `student`, edite com `vim`:

`/home/student/rhcsa-lab/obj01-06/app.conf`

Faça as seguintes alterações:

1. Altere `environment=development` para `environment=production`.
2. Altere `workers=2` para `workers=8`.
3. Remova completamente a linha `debug=true`.
4. Adicione `logging=verbose` imediatamente após a linha `workers=8`.
5. Preserve a primeira linha de comentário e a linha `port=8080`.
6. Crie também `notes.txt` com exatamente estas três linhas:

```text
review completed
configuration updated
ready for validation
```

Não substitua o arquivo por outro pré-pronto; pratique a edição interativa no terminal.
