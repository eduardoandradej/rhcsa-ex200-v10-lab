Trabalhe inicialmente no `servera` como `student`.

Diretório do exercício:

`/home/student/rhcsa-lab/obj01-04`

1. A partir do `servera`, acesse `student@serverb` por SSH e grave o FQDN remoto em `remote-host.txt`.
2. A partir do `servera`, acesse novamente `student@serverb` e grave o nome do usuário remoto em `remote-user.txt`.
3. No `servera`, alterne para o usuário `labuser` usando uma shell de login. A senha desse usuário de laboratório é `redhat`.
4. Como `labuser`, crie `/home/labuser/switch-user.txt` contendo somente o resultado de `whoami`.
5. Encerre a sessão de `labuser` e retorne ao usuário `student`.

O objetivo é praticar conexão SSH e mudança real de identidade de usuário; não crie os arquivos manualmente com valores digitados.
