No `servera`, crie `/etc/tmpfiles.d/rhcsa-momentary.conf` para garantir:

```text
diretório:   /run/rhcsa-momentary
modo:        0700
usuário:     root
grupo:       root
idade:       30s
```

Use o tipo `d`.

Depois:

1. aplique a regra com `systemd-tmpfiles --create`;
2. crie `/run/rhcsa-momentary/stale.txt`;
3. deixe o arquivo permanecer sem uso por mais de 30 segundos;
4. execute `systemd-tmpfiles --clean` usando somente esse arquivo de regra;
5. salve `stat -c '%a %U %G %n' /run/rhcsa-momentary`
   em `output/stat.txt`.

Estado final: diretório correto e `stale.txt` removido.
