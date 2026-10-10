Configure um mapa **indireto** do AutoFS com base `/remote11`.

Use:

- `/etc/auto.master.d/rhcsa11.autofs`;
- `/etc/auto.rhcsa11`;
- wildcard `*` no mapa;
- `&` para substituir a chave no caminho remoto;
- origem `serverb:/srv/rhcsa11/projects/&`;
- opções `rw,sync,fstype=nfs`.

Habilite e inicie o AutoFS. Depois acesse `alpha` e `beta`.

Grave os dois conteúdos em `output/content.txt` e as montagens em
`output/findmnt.txt`.
