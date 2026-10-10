O `servera` foi deixado em modo SELinux permissivo, tanto no estado atual
quanto na configuração de boot.

Deixe o sistema com:

1. SELinux **Enforcing** agora.
2. `SELINUX=enforcing` em `/etc/selinux/config`.
3. Grave `getenforce` em `output/getenforce.txt`.
4. Grave a linha `SELINUX=` em `output/config.txt`.

Não desabilite o SELinux.
