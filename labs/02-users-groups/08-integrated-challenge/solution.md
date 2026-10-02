# Solução possível — obj02-08

```bash
sudo sed -ri 's/^[[:space:]]*PASS_MAX_DAYS[[:space:]]+.*/PASS_MAX_DAYS 30/' /etc/login.defs

sudo groupadd -g 35050 consultantsx

echo '%consultantsx ALL=(ALL) ALL' | sudo tee /etc/sudoers.d/consultantsx
sudo chmod 0440 /etc/sudoers.d/consultantsx
sudo visudo -cf /etc/sudoers.d/consultantsx

for u in consultx1 consultx2 consultx3; do
  sudo useradd -G consultantsx "$u"
done

printf 'consultx1:redhat\nconsultx2:redhat\nconsultx3:redhat\n' | sudo chpasswd

EXP="$(date -d '+90 days' +%F)"
for u in consultx1 consultx2 consultx3; do
  sudo chage -E "$EXP" -d 0 "$u"
done

sudo chage -M 15 consultx2
```
