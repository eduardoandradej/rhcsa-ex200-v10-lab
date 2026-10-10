Configure uma montagem automática **direta** para
`serverb:/srv/rhcsa11/direct` em `/home/student/direct11`.

Use:

- `/etc/auto.master.d/rhcsa11.autofs` como mapa mestre;
- `/etc/auto.rhcsa11` como mapa direto;
- `rw,sync` e tipo NFS;
- serviço `autofs` habilitado e ativo.

Acesse `/home/student/direct11/hello.txt` para disparar a montagem e grave:

1. o conteúdo em `output/content.txt`;
2. `findmnt -T /home/student/direct11/hello.txt` em `output/findmnt.txt`;
3. o estado do serviço em `output/service.txt`.
