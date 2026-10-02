# SSH baseline entre os nós gerenciados

Os exercícios que exigem acesso remoto de `servera` para `serverb` precisam de
um caminho SSH previsível, assim como ocorre em um ambiente de treinamento.

Antes desses labs, o `setup` garante:

- chave Ed25519 do usuário `student` no `servera`;
- chave pública autorizada para `student` no `serverb`;
- `known_hosts` do `servera` atualizado com as chaves atuais do `serverb`;
- validação não interativa com `ssh -o BatchMode=yes`.

Essa preparação pertence à infraestrutura do lab. O estudante continua
praticando o comando `ssh`, execução de comandos remotos e redirecionamentos,
sem o exercício depender de prompts de senha ou de chaves antigas após reset
das VMs.

A regressão de referência deve usar SSH real. Não é permitido simular o
resultado remoto escrevendo diretamente o hostname esperado em um arquivo.
