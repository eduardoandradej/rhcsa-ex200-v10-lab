# RHCSA EX200 v10 — Gabarito Operacional

## Objective 02 — Users & Groups

**Referência:** repositório `eduardoandradej/rhcsa-ex200-v10-lab`, branch `main`.  
**Plataforma local:** RHEL 9.8 • **Referência do exame:** RHEL 10.  
**Execução:** `lab start`, `lab grade` e `lab finish` sempre no `bastion`. As tarefas são realizadas como `student` nos servidores indicados, utilizando `sudo` quando necessário.  
**Sequência:** execute um laboratório por vez; só finalize depois de conferir o resultado do `lab grade`.

---

### obj02-01 — Identidade e bases locais

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj02-01
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj02-01
id acctalpha > output/acctalpha-id.txt
getent passwd acctbeta > output/acctbeta-passwd.txt
getent group auditgrp > output/auditgrp-group.txt
getent passwd acctalpha | cut -d: -f1,3,4,6,7 > output/acctalpha-fields.txt
exit
```

**No bastion, execute:**

```bash
lab grade obj02-01
lab finish obj02-01
```

---

### obj02-02 — Criar, modificar e remover usuários

**No bastion, execute:**

```bash
lab start obj02-02
ssh student@servera
```

**No servera, execute:**

```bash
sudo useradd -u 2301 -c 'Operations Alpha' -s /bin/bash opsalpha
sudo useradd -c 'Operations Beta' opsbeta
sudo usermod -d /srv/opsbeta -m opsbeta
sudo useradd opstemp
sudo userdel -r opstemp
exit
```

**No bastion, execute:**

```bash
lab grade obj02-02
lab finish obj02-02
```

---

### obj02-03 — Criar e modificar grupos

**No bastion, execute:**

```bash
lab start obj02-03
ssh student@servera
```

**No servera, execute:**

```bash
sudo groupadd -g 33010 linuxops
sudo groupadd auditteam
sudo groupadd -g 33021 devtemp
sudo groupmod -n devopsgrp devtemp
sudo groupmod -g 33022 devopsgrp
sudo groupadd oldgrp
sudo groupdel oldgrp
exit
```

**No bastion, execute:**

```bash
lab grade obj02-03
lab finish obj02-03
```

---

### obj02-04 — Grupos primários e suplementares

**No bastion, execute:**

```bash
lab start obj02-04
ssh student@servera
```

**No servera (`student`), execute:**

```bash
sudo usermod -aG projecta teamuser1
sudo usermod -aG projecta teamuser2
sudo usermod -g projectb teamuser2
sudo -iu teamuser1
```

**No servera (`teamuser1`), execute:**

```bash
newgrp projecta
touch /home/teamuser1/projecta-owned.txt
exit
exit
exit
```

**No bastion, execute:**

```bash
lab grade obj02-04
lab finish obj02-04
```

---

### obj02-05 — Senhas e password aging

**No bastion, execute:**

```bash
lab start obj02-05
ssh student@servera
```

**No servera, execute:**

```bash
printf 'aginguser1:redhat\naginguser2:redhat\n' | sudo chpasswd
sudo chage -m 2 -M 45 -W 7 -I 5 aginguser1
sudo chage -d 0 aginguser1
sudo chage -M 90 aginguser2
sudo chage -E "$(date -d '+90 days' +%F)" aginguser2
exit
```

**No bastion, execute:**

```bash
lab grade obj02-05
lab finish obj02-05
```

---

### obj02-06 — Sudo e sudoers.d

**No bastion, execute:**

```bash
lab start obj02-06
ssh student@servera
```

**No servera, execute:**

```bash
sudo usermod -aG opsadmin svcadmin
printf '%s\n' '%opsadmin ALL=(root) NOPASSWD: /usr/bin/id, /usr/bin/whoami' | sudo tee /etc/sudoers.d/opsadmin
sudo chmod 0440 /etc/sudoers.d/opsadmin
sudo visudo -cf /etc/sudoers.d/opsadmin
sudo -u svcadmin sudo -n /usr/bin/id -u
sudo -u svcadmin sudo -n /usr/bin/whoami
exit
```

**No bastion, execute:**

```bash
lab grade obj02-06
lab finish obj02-06
```

---

### obj02-07 — Lock, expiração e nologin

**No bastion, execute:**

```bash
lab start obj02-07
ssh student@servera
```

**No servera, execute:**

```bash
sudo usermod -L -e 1 departed1
sudo usermod -s /sbin/nologin serviceacct
sudo usermod -e "$(date -d '+30 days' +%F)" tempcontract
sudo usermod -U -e '' recoveruser
exit
```

**No bastion, execute:**

```bash
lab grade obj02-07
lab finish obj02-07
```

---

### obj02-08 — Desafio integrado Users & Groups

**No bastion, execute:**

```bash
lab start obj02-08
ssh student@serverb
```

**No serverb, execute:**

```bash
sudo sed -ri 's/^[[:space:]]*PASS_MAX_DAYS[[:space:]]+.*/PASS_MAX_DAYS 30/' /etc/login.defs
sudo groupadd -g 35050 consultantsx
printf '%s\n' '%consultantsx ALL=(ALL) ALL' | sudo tee /etc/sudoers.d/consultantsx
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
exit
```

**No bastion, execute:**

```bash
lab grade obj02-08
lab finish obj02-08
```

---

**Fim do Objective 02 — 8/8 laboratórios.**

> **Uso:** gabarito de consulta/correção. Execute somente dentro das VMs isoladas do projeto, após `lab start`. As senhas `redhat` são didáticas e não devem ser usadas fora desse ambiente.
