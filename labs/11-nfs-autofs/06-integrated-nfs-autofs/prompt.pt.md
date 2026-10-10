## Desafio integrado

Primeiro valide manualmente o NFS:

1. Monte `serverb:/srv/rhcsa11/integrated` em `/mnt/rhcsa11-check`.
2. Grave `findmnt /mnt/rhcsa11-check` em `output/manual.txt`.
3. Liste o conteúdo em `output/list.txt`.
4. Desmonte `/mnt/rhcsa11-check`.

Depois configure AutoFS indireto:

5. Base `/remote11-final`.
6. Mapa mestre `/etc/auto.master.d/rhcsa11.autofs`.
7. Mapa `/etc/auto.rhcsa11`.
8. Use wildcard para montar `serverb:/srv/rhcsa11/integrated/&`.
9. Opções `rw,sync,fstype=nfs`.
10. Habilite e inicie `autofs`.
11. Acesse as chaves `red` e `hat`.
12. Grave os conteúdos em `output/content.txt` e as montagens em
    `output/findmnt.txt`.

O estado final deve manter o AutoFS funcional.
