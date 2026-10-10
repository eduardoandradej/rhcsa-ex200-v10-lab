```bash
cd /home/student/rhcsa-lab/obj10-05

sudo ausearch -if input/avc.audit -m AVC > output/avc.txt

sudo semanage fcontext -a -t httpd_sys_content_t '/srv/avc10(/.*)?'
sudo restorecon -Rv /srv/avc10

ls -Zd /srv/avc10 /srv/avc10/index.html > output/context.txt
curl -sS http://127.0.0.1/avc10/index.html > output/curl.txt
```

Em uma máquina limpa/RHLS, a busca equivalente no log ativo continua sendo:

```bash
sudo ausearch -m AVC -ts recent
```

A adaptação local usa `-if` somente para evitar uma varredura custosa de um
`audit.log` que acumula muitas execuções automatizadas.
