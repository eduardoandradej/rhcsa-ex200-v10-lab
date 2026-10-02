## Desafio integrado — Users & Groups

No `serverb`, como `student`, use privilégios administrativos para atingir o seguinte estado:

1. Configure `PASS_MAX_DAYS` como `30` em `/etc/login.defs`.
2. Crie o grupo `consultantsx` com GID `35050`.
3. Crie `/etc/sudoers.d/consultantsx`, modo `0440`, permitindo aos membros de `consultantsx` executar qualquer comando como qualquer usuário.
4. Crie `consultx1`, `consultx2` e `consultx3` com `consultantsx` como grupo suplementar.
5. Defina a senha de laboratório `redhat` para as três contas.
6. Faça as três contas expirarem 90 dias a partir da data atual.
7. Em `consultx2`, configure máximo de 15 dias para a senha.
8. Force as três contas a trocar a senha no próximo login.
9. Valide o arquivo sudoers com `visudo`.

O `lab finish` restaurará `/etc/login.defs` para o estado anterior ao exercício.
