## Cenário

Uma nova equipe de operações precisa de uma conta local e de uma área
compartilhada. Entregue o seguinte estado final no `servera`:

- grupo `ops12`;
- usuário `analyst12`, shell `/bin/bash`, membro suplementar de `ops12`;
- política de senha de `analyst12`: mínimo 2 dias, máximo 45 dias e aviso 7 dias;
- diretório `/srv/team12`, proprietário `root:ops12`, modo `2770`;
- ACL concedendo `rwx` ao usuário `student`;
- dois arquivos regulares: `/srv/team12/alpha.txt` e `/srv/team12/beta.txt`;
- `/usr/local/bin/count-team12`, executável, recebendo um diretório como
  primeiro argumento e imprimindo somente a quantidade de arquivos regulares
  existentes diretamente nesse diretório.

Ao final, grave:

- `id analyst12` em `output/id.txt`;
- `chage -l analyst12` em `output/chage.txt`;
- `getfacl -p /srv/team12` em `output/acl.txt`;
- a execução `count-team12 /srv/team12` em `output/count.txt`.

O resultado esperado do contador é `2`.
