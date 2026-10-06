```bash
cd /home/student/rhcsa-lab/obj07-02

echo 'd /run/rhcsa-momentary 0700 root root 30s' | \
  sudo tee /etc/tmpfiles.d/rhcsa-momentary.conf

sudo systemd-tmpfiles --create /etc/tmpfiles.d/rhcsa-momentary.conf
sudo touch /run/rhcsa-momentary/stale.txt

sleep 35

sudo systemd-tmpfiles --clean /etc/tmpfiles.d/rhcsa-momentary.conf

stat -c '%a %U %G %n' /run/rhcsa-momentary > output/stat.txt
```

Neste teste, o arquivo precisa envelhecer de verdade. Retrodatação artificial
de `mtime`/`atime` não é um substituto confiável porque o `ctime` continua
recente.
