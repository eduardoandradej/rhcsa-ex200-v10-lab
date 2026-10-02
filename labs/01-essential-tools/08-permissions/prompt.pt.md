No `servera`, como `student`, trabalhe em:

`/home/student/rhcsa-lab/obj01-08`

1. Ajuste `data/report.txt` para que o proprietário tenha leitura e escrita, o grupo tenha somente leitura e outros não tenham acesso.
2. Ajuste `data/scripts` para `rwx` para o proprietário, `rx` para o grupo e nenhum acesso para outros.
3. Em `data/scripts/backup.sh`, adicione permissão de execução somente ao proprietário, preservando as demais permissões existentes.
4. Na shell atual, defina `umask 0027`.
5. Com essa `umask`, crie `generated/new-file.txt` e `generated/new-dir`.
6. Não altere manualmente as permissões dos dois objetos criados no passo anterior; o resultado deve vir da `umask`.

Ao terminar, retorne ao bastion e execute `lab grade obj01-08`.
