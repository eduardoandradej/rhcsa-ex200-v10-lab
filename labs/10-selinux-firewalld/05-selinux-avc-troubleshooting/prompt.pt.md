O Apache está configurado para publicar `/srv/avc10` em
`http://127.0.0.1/avc10/`, mas o SELinux impede o acesso.

O ambiente já capturou uma pequena amostra **real** do AVC em
`input/avc.audit`. Isso evita que o laboratório dependa do tamanho acumulado
do `/var/log/audit/audit.log`.

1. Confirme que SELinux permanece `Enforcing`.
2. Analise `input/avc.audit` com `ausearch` e grave o resultado em
   `output/avc.txt`.
3. Identifique o processo, o caminho negado e o tipo SELinux incorreto.
4. Corrija a causa pela política persistente de contexto de arquivo, sem
   desabilitar SELinux e sem gerar módulo de política local.
5. Faça `/srv/avc10` e seu conteúdo terem `httpd_sys_content_t`.
6. Grave o contexto final em `output/context.txt`.
7. Grave o conteúdo retornado por
   `curl http://127.0.0.1/avc10/index.html` em `output/curl.txt`.

Não use `audit2allow` como atalho.
