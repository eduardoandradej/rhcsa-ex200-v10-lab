## Cenário

Entregue o `servera` pronto para uma rotina operacional:

- `httpd` habilitado e ativo;
- `/var/www/html/ops12.html` contendo exatamente `OBJ12 operations ready`;
- `/etc/cron.d/ops12` executando `/usr/bin/date >> /home/student/ops12-cron.log`
  como `student` a cada 10 minutos;
- `/etc/tmpfiles.d/ops12.conf` criando `/run/ops12` com modo `0750`,
  proprietário `student:student`;
- rsyslog roteando mensagens `local6.*` para `/var/log/ops12.log`;
- envie uma mensagem com facility `local6` contendo `OBJ12 operations ready`
  e confirme que ela chegou ao arquivo de log.

Grave em `output/`:

- `curl.txt`: conteúdo servido pelo Apache;
- `httpd.txt`: estado ativo e habilitado do `httpd`;
- `cron.txt`: conteúdo do arquivo de cron;
- `tmpfiles.txt`: `stat` de `/run/ops12`;
- `log.txt`: linha do log que contém a mensagem de teste.
