# RHCSA EX200 v10 — Gabarito Operacional

## Objective 07 — Scheduling, Temporary Files, Logging & Time

**Referência:** repositório [`eduardoandradej/rhcsa-ex200-v10-lab`](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab), branch `main` — enunciados `prompt.pt.md`, scripts `tests/reference-solutions/obj07-*.sh` e graders do Objective 07.  
**Plataforma local:** RHEL 9.8 • **Referência do exame:** RHEL 10.  
**Execução:** execute `lab start`, `lab grade` e `lab finish` no `bastion`. Execute os comandos como `student` no nó indicado.  
**Sequência:** um laboratório por vez; confirme `lab grade` antes de executar `lab finish`.

---

### obj07-01 — Gerenciar tarefa recorrente com systemd timer

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj07-01
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj07-01

systemctl cat sysstat-collect.timer
systemctl cat sysstat-collect.service

sudo cp /usr/lib/systemd/system/sysstat-collect.timer \
  /etc/systemd/system/sysstat-collect.timer

sudo sed -i 's#OnCalendar=.*#OnCalendar=*:00/2#' \
  /etc/systemd/system/sysstat-collect.timer

sudo systemctl daemon-reload
sudo systemctl enable --now sysstat-collect.timer

systemctl cat sysstat-collect.timer > output/timer.txt
systemctl list-timers sysstat-collect.timer --all --no-pager > output/list-timers.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj07-01
lab finish obj07-01
```

---

### obj07-02 — Gerenciar arquivos temporários com systemd-tmpfiles

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj07-02
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj07-02

printf '%s\n' 'd /run/rhcsa-momentary 0700 root root 30s' | \
  sudo tee /etc/tmpfiles.d/rhcsa-momentary.conf > /dev/null

sudo systemd-tmpfiles --create /etc/tmpfiles.d/rhcsa-momentary.conf
sudo touch /run/rhcsa-momentary/stale.txt

sleep 35

sudo systemd-tmpfiles --clean /etc/tmpfiles.d/rhcsa-momentary.conf

stat -c '%a %U %G %n' /run/rhcsa-momentary > output/stat.txt

sudo test ! -e /run/rhcsa-momentary/stale.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj07-02
lab finish obj07-02
```

---

### obj07-03 — Agendar tarefa recorrente em /etc/cron.d

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj07-03
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj07-03

sudo tee /etc/cron.d/rhcsa-report > /dev/null <<'EOF'
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root
*/5 * * * * student /usr/bin/id -un >> /home/student/rhcsa-lab/obj07-03/cron-run.txt
EOF

sudo chmod 0644 /etc/cron.d/rhcsa-report
sudo cat /etc/cron.d/rhcsa-report > output/cron.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj07-03
lab finish obj07-03
```

---

### obj07-04 — Roteamento de eventos com rsyslog

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj07-04
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj07-04

printf '%s\n' 'local6.debug /var/log/rhcsa-debug.log' | \
  sudo tee /etc/rsyslog.d/rhcsa-debug.conf > /dev/null

sudo rsyslogd -N1
sudo systemctl restart rsyslog

logger -p local6.debug -t obj07-rsyslog 'OBJ07-RSYSLOG-DEBUG'
sleep 1

sudo tail -n 20 /var/log/rhcsa-debug.log > output/log.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj07-04
lab finish obj07-04
```

---

### obj07-05 — Filtrar eventos com journalctl

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj07-05
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj07-05

journalctl -t obj07-journal --since '-10 min' --no-pager > output/tag.txt

journalctl -t obj07-journal -p warning --since '-10 min' --no-pager > output/warning.txt

journalctl _SYSTEMD_UNIT=rhcsa-journal.service --no-pager > output/unit.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj07-05
lab finish obj07-05
```

---

### obj07-06 — Configurar journal persistente

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj07-06
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj07-06

sudo mkdir -p /etc/systemd/journald.conf.d

sudo tee /etc/systemd/journald.conf.d/99-rhcsa-persistent.conf > /dev/null <<'EOF'
[Journal]
Storage=persistent
SystemMaxUse=100M
EOF

sudo mkdir -p /var/log/journal
sudo systemctl restart systemd-journald
sudo journalctl --flush

journalctl --list-boots --no-pager > output/boots.txt
journalctl --disk-usage > output/disk-usage.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj07-06
lab finish obj07-06
```

---

### obj07-07 — Configurar fuso horário e verificar Chrony

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj07-07
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj07-07

sudo timedatectl set-timezone America/Jamaica
sudo timedatectl set-ntp true
sudo systemctl enable --now chronyd

timedatectl > output/timedatectl.txt
chronyc sources -v > output/sources.txt
chronyc tracking > output/tracking.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj07-07
lab finish obj07-07
```

---

### obj07-08 — Desafio integrado de scheduling e logs

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj07-08
ssh student@serverb
```

**No serverb, execute:**

```bash
cd /home/student/rhcsa-lab/obj07-08

printf '%s\n' 'local5.notice /var/log/rhcsa-audit.log' | \
  sudo tee /etc/rsyslog.d/rhcsa-audit.conf > /dev/null

sudo tee /etc/systemd/system/rhcsa-audit.service > /dev/null <<'EOF'
[Unit]
Description=RHCSA audit marker

[Service]
Type=oneshot
ExecStart=/usr/bin/logger -p local5.notice -t rhcsa-audit OBJ07-INTEGRATED-AUDIT
EOF

sudo tee /etc/systemd/system/rhcsa-audit.timer > /dev/null <<'EOF'
[Unit]
Description=RHCSA audit timer

[Timer]
OnBootSec=1min
OnUnitActiveSec=5min
Unit=rhcsa-audit.service

[Install]
WantedBy=timers.target
EOF

sudo rsyslogd -N1
sudo systemctl restart rsyslog
sudo systemctl daemon-reload
sudo systemctl enable --now rhcsa-audit.timer
sudo systemctl start rhcsa-audit.service

sudo journalctl --sync
sleep 1

systemctl status rhcsa-audit.timer --no-pager > output/timer.txt
sudo tail -n 20 /var/log/rhcsa-audit.log > output/syslog.txt
journalctl -t rhcsa-audit --since '-10 min' --no-pager > output/journal.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj07-08
lab finish obj07-08
```

---

## Referências de consulta

- [Enunciados — Objective 07](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab/tree/main/labs/07-scheduling-logs)
- [Soluções de referência — obj07-01 a obj07-08](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab/tree/main/tests/reference-solutions)

**Validação:** comandos confrontados com os enunciados e scripts de referência publicados na branch `main` em 12/10/2026. A sintaxe dos blocos Bash foi verificada. **Não houve execução dos laboratórios nem confirmação de pontuação nas VMs nesta sessão.**
