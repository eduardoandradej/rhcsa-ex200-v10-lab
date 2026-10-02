# Hotfix 0.6.6 — obj01-05 alinhado à baseline

Depois da introdução da baseline global de dependências, o `obj01-05` não deve
mais tentar localizar ou instalar `bzip2` durante `lab start`.

O exercício agora apenas valida:

```text
tar
gzip
bzip2
```

Se algum deles estiver ausente, o problema é da preparação da infraestrutura e
deve ser corrigido pelo bootstrap global:

```bash
bash bootstrap/20-install-dependencies.sh
```

Isso mantém a separação:

```text
infraestrutura -> instala dependências
lab start       -> prepara somente o cenário do exercício
```
