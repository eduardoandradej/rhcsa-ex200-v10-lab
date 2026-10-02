# Solução possível — obj02-04

```bash
sudo usermod -aG projecta teamuser1
sudo usermod -aG projecta teamuser2
sudo usermod -g projectb teamuser2

sudo -iu teamuser1
newgrp projecta
touch /home/teamuser1/projecta-owned.txt
exit
exit
```
