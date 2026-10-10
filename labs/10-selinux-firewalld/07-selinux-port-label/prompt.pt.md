O Apache possui uma configuração adicional para escutar em `48888/tcp`, mas
está parado.

1. Configure o SELinux para permitir que `httpd` use `48888/tcp` com o tipo
   `http_port_t`.
2. Inicie o Apache.
3. Grave a customização local de portas SELinux em `output/ports.txt`.
4. Grave a escuta TCP do Apache em `output/listen.txt`.

Não desabilite SELinux e não coloque o sistema em permissive.
