# Solução possível — obj02-06

```bash
sudo usermod -aG opsadmin svcadmin
echo '%opsadmin ALL=(root) NOPASSWD: /usr/bin/id, /usr/bin/whoami'   | sudo tee /etc/sudoers.d/opsadmin
sudo chmod 0440 /etc/sudoers.d/opsadmin
sudo visudo -cf /etc/sudoers.d/opsadmin
sudo -u svcadmin sudo -n /usr/bin/id -u
```
