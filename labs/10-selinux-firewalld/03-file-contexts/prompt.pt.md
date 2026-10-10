O diretório `/srv/web10` contém conteúdo que deve ser servido pelo Apache, mas
possui um contexto SELinux inadequado.

1. Crie uma regra persistente para `/srv/web10` e todo o conteúdo abaixo dele
   com tipo `httpd_sys_content_t`.
2. Aplique o contexto definido pela política.
3. Grave `ls -Zd /srv/web10` e `ls -Z /srv/web10/index.html` em
   `output/contexts.txt`.
4. Grave a customização local correspondente em `output/fcontext.txt`.

A solução deve sobreviver a um novo `restorecon`.
