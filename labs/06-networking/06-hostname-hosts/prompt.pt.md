No `servera`:

1. altere temporariamente o hostname para `temporary-net` e grave `hostname` em `output/temporary-hostname.txt`;
2. grave `/etc/hostname` em `output/static-before.txt`;
3. configure persistentemente `nodea.lab.test`;
4. adicione `10.66.6.254 peer06.lab.test peer06` ao `/etc/hosts`;
5. grave `getent hosts peer06` em `output/getent.txt`;
6. grave `ping -c 2 peer06` em `output/ping.txt`.

Estado final: hostname atual e estático `nodea.lab.test`. `lab finish` restaura tudo.
