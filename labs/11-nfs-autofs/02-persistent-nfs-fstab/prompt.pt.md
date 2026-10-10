Configure `serverb:/srv/rhcsa11/persist` para montagem persistente em
`/mnt/rhcsa11-persist`.

Requisitos:

1. Use `/etc/fstab`.
2. Tipo `nfs`.
3. Opções `rw,sync`.
4. Atualize o systemd após alterar o `fstab`.
5. Monte usando a entrada do `fstab`, sem repetir origem e opções no comando.
6. Grave `findmnt /mnt/rhcsa11-persist` em `output/findmnt.txt`.
7. Grave `findmnt --verify` em `output/verify.txt`.
8. Grave o conteúdo remoto em `output/content.txt`.

A montagem deve permanecer ativa ao final do exercício.
