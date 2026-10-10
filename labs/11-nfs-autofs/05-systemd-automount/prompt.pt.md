Configure uma montagem NFS sob demanda usando o **gerador de unidades do
systemd a partir do `/etc/fstab`**, não o serviço AutoFS.

1. Origem: `serverb:/srv/rhcsa11/systemd`.
2. Destino: `/mnt/rhcsa11-auto`.
3. Tipo: `nfs`.
4. Opções: `rw,sync,x-systemd.automount`.
5. Recarregue o daemon.
6. Inicie a unidade `.automount` correspondente ao caminho.
7. Grave o estado da unidade em `output/unit.txt`.
8. Acesse `hello.txt` para disparar o mount.
9. Grave `findmnt -T /mnt/rhcsa11-auto/hello.txt` em `output/findmnt.txt`.
10. Grave o conteúdo em `output/content.txt`.
