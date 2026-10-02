```bash
sudo tee /etc/yum.repos.d/rhcsa-custom.repo >/dev/null <<'EOF'
[rhcsa-custom]
name=RHCSA Custom Repository
baseurl=file:///var/lib/rhcsa-lab/obj03/repos/base
enabled=1
gpgcheck=0
EOF

sudo dnf clean metadata
dnf repolist
dnf --disablerepo='*' --enablerepo=rhcsa-custom list rhcsa-toolkit
```
