# Solução possível — obj02-05

Uma solução automatizável para referência:

```bash
printf 'aginguser1:redhat\naginguser2:redhat\n' | sudo chpasswd
sudo chage -m 2 -M 45 -W 7 -I 5 aginguser1
sudo chage -d 0 aginguser1
sudo chage -M 90 aginguser2
sudo chage -E "$(date -d '+90 days' +%F)" aginguser2
```

Durante o estudo manual, pratique também `passwd` e `chage -l`.
