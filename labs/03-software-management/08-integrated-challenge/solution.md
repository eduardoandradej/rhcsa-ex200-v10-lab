# Solução possível — obj03-08

```bash
cd /home/student/rhcsa-lab/obj03-08

sudo tee /etc/yum.repos.d/rhcsa-system.repo >/dev/null <<'EOF'
[rhcsa-system-base]
name=RHCSA System Base
baseurl=file:///var/lib/rhcsa-lab/obj03/repos/base
enabled=1
gpgcheck=0

[rhcsa-system-errata]
name=RHCSA System Errata
baseurl=file:///var/lib/rhcsa-lab/obj03/repos/errata
enabled=0
gpgcheck=0
EOF

sudo dnf -y --disablerepo='*' --enablerepo=rhcsa-system-base \
  install rhcsa-system-1.0-1

rpm -qpi assets/rhcsa-local-1.0-1.noarch.rpm \
  > output/local-rpm-info.txt

sudo dnf -y install ./assets/rhcsa-local-1.0-1.noarch.rpm

sudo sed -i '/^\[rhcsa-system-errata\]/,/^\[/ s/^enabled=.*/enabled=1/' \
  /etc/yum.repos.d/rhcsa-system.repo

sudo dnf -y --disablerepo='*' \
  --enablerepo=rhcsa-system-base \
  --enablerepo=rhcsa-system-errata \
  upgrade rhcsa-system

sudo sed -i 's/^enabled=1/enabled=0/g' \
  /etc/yum.repos.d/rhcsa-system.repo

id="$(dnf history list rhcsa-system \
  | awk '$1 ~ /^[0-9]+$/ {print $1; exit}')"

dnf history info "$id" > output/history.txt
```
