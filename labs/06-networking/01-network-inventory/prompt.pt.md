No `servera`, trabalhe em `/home/student/rhcsa-lab/obj06-01`.

O setup criou as interfaces isoladas `ex200a` e `ex200b`. Elas não transportam a sessão SSH.
Sem modificar a rede, produza:

```text
output/devices.txt       # nmcli device status
output/connections.txt   # nmcli connection show
output/active.txt        # somente perfis ativos
output/ex200a-link.txt   # ip -br link show ex200a
```

Objetivo: distinguir **device** de **connection profile** e identificar o que está ativo.
