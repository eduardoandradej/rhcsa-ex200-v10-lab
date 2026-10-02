# Solução possível — obj02-01

```bash
cd /home/student/rhcsa-lab/obj02-01
id acctalpha > output/acctalpha-id.txt
getent passwd acctbeta > output/acctbeta-passwd.txt
getent group auditgrp > output/auditgrp-group.txt
getent passwd acctalpha | cut -d: -f1,3,4,6,7 > output/acctalpha-fields.txt
```
