# Solução possível — obj02-03

```bash
sudo groupadd -g 33010 linuxops
sudo groupadd auditteam
sudo groupadd -g 33021 devtemp
sudo groupmod -n devopsgrp devtemp
sudo groupmod -g 33022 devopsgrp
sudo groupadd oldgrp
sudo groupdel oldgrp
```
