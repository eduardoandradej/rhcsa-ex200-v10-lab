# Solução possível — obj02-07

```bash
sudo usermod -L -e 1 departed1
sudo usermod -s /sbin/nologin serviceacct
sudo usermod -e "$(date -d '+30 days' +%F)" tempcontract
sudo usermod -U -e '' recoveruser
```
