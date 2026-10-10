No `servera`:

1. Consulte as exportações disponíveis no `serverb` e grave o resultado em
   `output/exports.txt`.
2. Monte `serverb:/srv/rhcsa11/manual` em `/mnt/rhcsa11-manual` como NFS,
   leitura/gravação e síncrono.
3. Grave `findmnt /mnt/rhcsa11-manual` em `output/mount.txt`.
4. Grave o conteúdo de `hello.txt` em `output/content.txt`.
5. Desmonte `/mnt/rhcsa11-manual`.
6. Grave uma evidência final em `output/unmounted.txt` que demonstre que o
   ponto não permanece montado.

O estado final deve estar desmontado.
