# Hotfix 0.6.4

O laboratório `obj01-05` agora resolve a dependência `bzip2` diretamente a
partir dos `baseurl=file://` configurados nos repositórios DNF do bastion.

Isso evita depender de um caminho de montagem presumido para a mídia RHEL.

O fluxo agora é:

1. verificar `tar`, `gzip` e `bzip2`;
2. se `bzip2` estiver ausente, ler `/etc/yum.repos.d/*.repo`;
3. localizar o RPM no `file://` real do repositório;
4. copiar o RPM para `servera`;
5. instalar localmente;
6. validar as ferramentas;
7. preparar o exercício.
