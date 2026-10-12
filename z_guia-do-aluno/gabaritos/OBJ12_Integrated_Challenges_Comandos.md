# RHCSA EX200 v10 — Gabarito Operacional

## Objective 12 — Comprehensive EX200 Challenges

**Referência:** repositório [`eduardoandradej/rhcsa-ex200-v10-lab`](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab), branch `main` — enunciados, critérios e scripts `tests/reference-solutions/obj12-*.sh` dos seis laboratórios.  
**Plataforma local:** RHEL 9.8 • **Referência do exame:** RHEL 10.  
**Execução:** use o `bastion` para `lab start`, `lab grade` e `lab finish`; execute a resolução no `servera` como `student`. O `serverb` fornece o export NFS do `obj12-06` preparado pelo ambiente.  
**Sequência:** um laboratório por vez; execute `lab grade` antes de `lab finish`.  
**Segurança:** os comandos de storage do `obj12-03` apagam dados em `/dev/vdb`. Execute somente na VM `servera` do laboratório, após `lab start` e conferência do disco. Nunca execute em `/dev/vda` nem em um sistema de produção.

[Índice dos gabaritos](README.md) · [OBJ11 — Anterior](OBJ11_NFS_AutoFS_Comandos.md)

---

### obj12-01 — Desafio final de usuários, permissões, ACL e shell

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj12-01
ssh student@servera
```

**No servera, execute:**

```bash
sudo groupadd ops12
sudo useradd -m -s /bin/bash -G ops12 analyst12
sudo chage -m 2 -M 45 -W 7 analyst12

sudo mkdir -p /srv/team12
sudo chown root:ops12 /srv/team12
sudo chmod 2770 /srv/team12
sudo setfacl -m u:student:rwx /srv/team12

sudo touch /srv/team12/alpha.txt /srv/team12/beta.txt
sudo chown root:ops12 /srv/team12/alpha.txt /srv/team12/beta.txt
sudo chmod 0660 /srv/team12/alpha.txt /srv/team12/beta.txt

sudo tee /usr/local/bin/count-team12 >/dev/null <<'EOF'
#!/bin/bash
set -Eeuo pipefail
[[ $# -eq 1 && -d "$1" ]] || exit 2
find "$1" -maxdepth 1 -type f -printf '.' | wc -c
EOF
sudo chmod 0755 /usr/local/bin/count-team12

cd /home/student/rhcsa-lab/obj12-01
id analyst12 > output/id.txt
sudo chage -l analyst12 > output/chage.txt
getfacl -p /srv/team12 > output/acl.txt
/usr/local/bin/count-team12 /srv/team12 > output/count.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj12-01
lab finish obj12-01
```

---

### obj12-02 — Desafio final de serviços, agendamento e logs

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj12-02
ssh student@servera
```

**No servera, execute:**

```bash
sudo sh -c 'printf "%s\n" "OBJ12 operations ready" > /var/www/html/ops12.html'
sudo systemctl enable --now httpd

echo '*/10 * * * * student /usr/bin/date >> /home/student/ops12-cron.log' | sudo tee /etc/cron.d/ops12 >/dev/null
sudo chmod 0644 /etc/cron.d/ops12

echo 'd /run/ops12 0750 student student -' | sudo tee /etc/tmpfiles.d/ops12.conf >/dev/null
sudo systemd-tmpfiles --create /etc/tmpfiles.d/ops12.conf

echo 'local6.* /var/log/ops12.log' | sudo tee /etc/rsyslog.d/ops12.conf >/dev/null
sudo systemctl restart rsyslog
logger -p local6.notice -t obj12 'OBJ12 operations ready'
sleep 1

cd /home/student/rhcsa-lab/obj12-02
curl -sS http://127.0.0.1/ops12.html > output/curl.txt
{ systemctl is-active httpd; systemctl is-enabled httpd; } > output/httpd.txt
cat /etc/cron.d/ops12 > output/cron.txt
stat -c '%a %U %G %n' /run/ops12 > output/tmpfiles.txt
sudo grep 'OBJ12 operations ready' /var/log/ops12.log | tail -1 > output/log.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj12-02
lab finish obj12-02
```

---

### obj12-03 — Desafio final de partição, LVM, XFS e swap

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj12-03
ssh student@servera
```

**No servera, execute:**

```bash
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS /dev/vdb

sudo parted -s /dev/vdb mklabel gpt
sudo parted -s /dev/vdb mkpart primary 1MiB 3073MiB
sudo partprobe /dev/vdb || true
sudo udevadm settle --timeout=15 || true
for i in $(seq 1 15); do test -b /dev/vdb1 && break; sleep 1; done
test -b /dev/vdb1

sudo pvcreate -ff -y /dev/vdb1
sudo vgcreate vg12 /dev/vdb1
sudo lvcreate --yes --wipesignatures y -L 1024M -n lvdata vg12
sudo mkfs.xfs -f -L DATA12 /dev/vg12/lvdata
sudo lvextend -L +512M /dev/vg12/lvdata

sudo mkdir -p /srv/data12
DATA_UUID=$(sudo blkid -s UUID -o value /dev/vg12/lvdata)
echo "UUID=$DATA_UUID /srv/data12 xfs defaults 0 0" | sudo tee -a /etc/fstab >/dev/null

sudo lvcreate --yes --wipesignatures y -L 512M -n lvswap vg12
sudo mkswap -L SWAP12 /dev/vg12/lvswap
SWAP_UUID=$(sudo blkid -s UUID -o value /dev/vg12/lvswap)
echo "UUID=$SWAP_UUID none swap defaults 0 0" | sudo tee -a /etc/fstab >/dev/null

sudo systemctl daemon-reload
sudo mount -a
sudo xfs_growfs /srv/data12
sudo swapon -a

cd /home/student/rhcsa-lab/obj12-03
lsblk -f /dev/vdb > output/lsblk.txt
{ sudo pvs; sudo vgs; sudo lvs; } > output/lvm.txt
findmnt /srv/data12 > output/findmnt.txt
cat /proc/swaps > output/swap.txt
sudo findmnt --verify > output/verify.txt 2>&1

exit
```

**No bastion, execute:**

```bash
lab grade obj12-03
lab finish obj12-03
```

---

### obj12-04 — Desafio final de boot e manutenção persistente

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj12-04
ssh student@servera
```

**No servera, execute:**

```bash
sudo systemctl set-default multi-user.target
sudo grubby --update-kernel=ALL --args='systemd.show_status=1'

sudo mkdir -p /srv/boot12
echo 'tmpfs /srv/boot12 tmpfs rw,nosuid,nodev 0 0' | sudo tee -a /etc/fstab >/dev/null
sudo systemctl daemon-reload
sudo mount /srv/boot12

cd /home/student/rhcsa-lab/obj12-04
systemctl get-default > output/target.txt
sudo grubby --info=ALL > output/grubby.txt
findmnt /srv/boot12 > output/findmnt.txt
sudo findmnt --verify > output/verify.txt 2>&1

exit
```

**No bastion, execute:**

```bash
lab grade obj12-04
lab finish obj12-04
```

---

### obj12-05 — Desafio final de SELinux, firewall e Apache

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj12-05
ssh student@servera
```

**No servera, execute:**

```bash
sudo semanage fcontext -a -t httpd_sys_content_t '/srv/secure12(/.*)?'
sudo restorecon -Rv /srv/secure12
sudo semanage port -a -t http_port_t -p tcp 48890

IFACE=$(ip -o route show default | awk '{print $5; exit}')
ZONE=$(sudo firewall-cmd --get-zone-of-interface="$IFACE")
if [ -z "$ZONE" ] || [ "$ZONE" = "no zone" ]; then
  ZONE=$(sudo firewall-cmd --get-default-zone)
fi

sudo firewall-cmd --permanent --zone="$ZONE" --add-port=48890/tcp
sudo firewall-cmd --reload
sudo systemctl enable --now httpd

cd /home/student/rhcsa-lab/obj12-05
ls -Zd /srv/secure12 /srv/secure12/index.html > output/contexts.txt
sudo semanage port -l -C | grep 48890 > output/selinux-port.txt
sudo firewall-cmd --zone="$ZONE" --query-port=48890/tcp > output/firewall.txt
{ systemctl is-active httpd; systemctl is-enabled httpd; } > output/service.txt
curl -sS http://127.0.0.1:48890/secure12/index.html > output/curl.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj12-05
lab finish obj12-05
```

---

### obj12-06 — Simulado final integrado

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj12-06
ssh student@servera
```

**No servera, execute:**

```bash
sudo groupadd opsfinal12
sudo useradd -m -s /bin/bash -G opsfinal12 operator12
sudo mkdir -p /srv/final12
sudo chown root:opsfinal12 /srv/final12
sudo chmod 2770 /srv/final12

echo '/remote12-final /etc/auto.final12' | sudo tee /etc/auto.master.d/final12.autofs >/dev/null
echo '* -rw,sync,fstype=nfs serverb:/srv/rhcsa11/integrated/&' | sudo tee /etc/auto.final12 >/dev/null
sudo systemctl enable --now autofs

sudo tee /usr/local/bin/final-report12 >/dev/null <<'EOF'
#!/bin/bash
set -Eeuo pipefail
[[ $# -eq 1 ]] || exit 2
key="$1"
case "$key" in red|hat) ;; *) exit 2 ;; esac
cat "/remote12-final/$key/info.txt" > "/srv/final12/report-$key.txt"
EOF
sudo chmod 0755 /usr/local/bin/final-report12

sudo -u operator12 /usr/local/bin/final-report12 red
sudo -u operator12 /usr/local/bin/final-report12 hat

echo '*/15 * * * * operator12 /usr/local/bin/final-report12 red' | sudo tee /etc/cron.d/final12 >/dev/null
sudo chmod 0644 /etc/cron.d/final12

cd /home/student/rhcsa-lab/obj12-06
id operator12 > output/id.txt
{ findmnt -T /remote12-final/red/info.txt; findmnt -T /remote12-final/hat/info.txt; } > output/mounts.txt
{ sudo cat /srv/final12/report-red.txt; sudo cat /srv/final12/report-hat.txt; } > output/reports.txt
cat /etc/cron.d/final12 > output/cron.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj12-06
lab finish obj12-06
```

---

[Voltar ao índice de gabaritos](README.md) · [OBJ11 — Anterior](OBJ11_NFS_AutoFS_Comandos.md)

**Fontes de referência:** [OBJ12 — Escopo, práticas e segurança](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab/blob/main/docs/OBJ12-COMPREHENSIVE.md) · [Soluções de QA do OBJ12](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab/tree/main/tests/reference-solutions)

> Comandos conferidos com os scripts de referência. Sintaxe Bash verificada; o resultado de `lab grade` exige execução no ambiente real.
