No `servera`:

1. Adicione `svcadmin` ao grupo suplementar `opsadmin`.
2. Crie `/etc/sudoers.d/opsadmin` com modo `0440`.
3. Autorize membros de `opsadmin` a executar, como `root` e sem senha, somente:
   - `/usr/bin/id`
   - `/usr/bin/whoami`
4. Valide a sintaxe da configuração com `visudo`.
5. Confirme que `svcadmin` consegue executar `sudo /usr/bin/id -u`.

Não altere diretamente `/etc/sudoers`.
