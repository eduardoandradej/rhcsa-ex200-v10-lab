# Solução possível — obj02-02

```bash
sudo useradd -u 2301 -c 'Operations Alpha' -s /bin/bash opsalpha
sudo useradd -c 'Operations Beta' opsbeta
sudo usermod -d /srv/opsbeta -m opsbeta
sudo useradd opstemp
sudo userdel -r opstemp
```
