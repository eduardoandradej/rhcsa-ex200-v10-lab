Uma solução portável entre o laboratório RHEL 9.8 e o alvo RHEL 10 é editar
persistentemente o parâmetro `enabled=`:

```bash
sudo sed -i '/^\[rhcsa-errata\]/,/^\[/ s/^enabled=.*/enabled=1/' \
  /etc/yum.repos.d/rhcsa-update.repo

sudo dnf -y upgrade rhcsa-update-demo
rpm -q rhcsa-update-demo

sudo sed -i 's/^enabled=1/enabled=0/g' \
  /etc/yum.repos.d/rhcsa-update.repo
```

No RHEL 10, pratique também `dnf config-manager --enable/--disable`.
