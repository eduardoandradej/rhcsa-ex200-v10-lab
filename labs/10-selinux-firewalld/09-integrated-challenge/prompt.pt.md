## Desafio integrado

Uma aplicação Apache deve publicar `/srv/rhcsa10-final` em
`48889/tcp`, mas o ambiente foi entregue incompleto.

Sem desabilitar SELinux e sem remover proteções existentes:

1. Garanta que `/srv/rhcsa10-final(/.*)?` use persistentemente
   `httpd_sys_content_t`.
2. Aplique os contextos corretos.
3. Autorize `48889/tcp` para `httpd` no SELinux com `http_port_t`.
4. Identifique a zona do firewalld usada pela interface da rota padrão.
5. Libere `48889/tcp` nessa zona de forma persistente e recarregue o firewall.
6. Inicie `httpd`.
7. Grave:
   - contextos em `output/contexts.txt`;
   - customização de porta SELinux em `output/selinux-port.txt`;
   - zona em `output/zone.txt`;
   - consulta runtime do firewall em `output/firewall.txt`;
   - resposta HTTP em `output/curl.txt`.

O conteúdo esperado da página é `OBJ10 integrated security PASS`.
