Habilite de forma **persistente** o Boolean SELinux
`httpd_enable_homedirs`.

Depois grave:

1. `getsebool httpd_enable_homedirs` em `output/getsebool.txt`.
2. A linha correspondente de `semanage boolean -l` em
   `output/semanage.txt`.
3. As customizações persistentes de Boolean em `output/custom.txt`.

A configuração deve continuar ativa após reboot.
