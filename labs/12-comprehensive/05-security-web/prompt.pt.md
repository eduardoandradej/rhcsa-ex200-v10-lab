## Cenário

O Apache deve disponibilizar `/srv/secure12` em
`http://127.0.0.1:48890/secure12/index.html`.

Entregue o estado:

- SELinux permanece `Enforcing`;
- `/srv/secure12(/.*)?` possui regra persistente
  `httpd_sys_content_t` e o contexto foi aplicado;
- `48890/tcp` possui tipo SELinux `http_port_t`;
- a porta `48890/tcp` está permitida de forma permanente na zona do
  firewalld usada pela interface da rota padrão;
- `httpd` está habilitado e ativo;
- a página responde `OBJ12 secure service ready`.

Grave em `output/`:

- `contexts.txt`;
- `selinux-port.txt`;
- `firewall.txt`;
- `service.txt`;
- `curl.txt`.
