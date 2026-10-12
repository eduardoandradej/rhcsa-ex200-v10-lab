# RHCSA EX200 v10 — Gabarito Operacional

## Objective 03 — RPM, DNF & Repositories

**Referência:** repositório [`eduardoandradej/rhcsa-ex200-v10-lab`](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab), branch `main` (enunciados, scripts de solução de referência e graders do Objective 03).  
**Plataforma local:** RHEL 9.8 • **Referência do exame:** RHEL 10.  
**Execução:** `lab start`, `lab grade` e `lab finish` sempre no `bastion`. Execute os comandos como `student` no servidor indicado e use `sudo` somente onde necessário.  
**Sequência:** execute um laboratório por vez; confira o resultado do `lab grade` antes do `lab finish`.

---

### obj03-01 — Consultar a base RPM instalada

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj03-01
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj03-01
rpm -q openssh-clients > output/package.txt
rpm -qf /usr/bin/ssh > output/owner.txt
rpm -qc openssh-clients > output/configs.txt
rpm -qd openssh-clients > output/docs.txt
rpm -ql openssh-clients > output/files.txt
exit
```

**No bastion, execute:**

```bash
lab grade obj03-01
lab finish obj03-01
```

---

### obj03-02 — Inspecionar e extrair um arquivo RPM

**No bastion, execute:**

```bash
lab start obj03-02
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj03-02
rpm -qpi rhcsa-inspect-1.0-1.noarch.rpm > output/info.txt
rpm -qpl rhcsa-inspect-1.0-1.noarch.rpm > output/files.txt
rpm -qpc rhcsa-inspect-1.0-1.noarch.rpm > output/configs.txt
rpm -qp --scripts rhcsa-inspect-1.0-1.noarch.rpm > output/scripts.txt
cd extracted
rpm2cpio ../rhcsa-inspect-1.0-1.noarch.rpm | cpio -id
exit
```

**No bastion, execute:**

```bash
lab grade obj03-02
lab finish obj03-02
```

---

### obj03-03 — Descobrir software com DNF

**No bastion, execute:**

```bash
lab start obj03-03
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj03-03
dnf search toolkit > output/search.txt
dnf info rhcsa-toolkit > output/info.txt
dnf provides /usr/local/share/rhcsa-toolkit/version.txt > output/provider.txt
dnf list rhcsa-toolkit > output/list.txt
exit
```

**No bastion, execute:**

```bash
lab grade obj03-03
lab finish obj03-03
```

---

### obj03-04 — Instalar e remover pacotes com DNF

**No bastion, execute:**

```bash
lab start obj03-04
ssh student@servera
```

**No servera, execute:**

```bash
sudo dnf -y install rhcsa-toolkit
sudo dnf -y install rhcsa-temp
rpm -q rhcsa-toolkit rhcsa-temp
sudo dnf -y remove rhcsa-temp
rpm -q rhcsa-toolkit
rpm -q rhcsa-temp || true
exit
```

**No bastion, execute:**

```bash
lab grade obj03-04
lab finish obj03-04
```

---

### obj03-05 — Configurar um repositório DNF

**No bastion, execute:**

```bash
lab start obj03-05
ssh student@servera
```

**No servera, execute:**

```bash
sudo tee /etc/yum.repos.d/rhcsa-custom.repo >/dev/null <<'EOF'
[rhcsa-custom]
name=RHCSA Custom Repository
baseurl=file:///var/lib/rhcsa-lab/obj03/repos/base
enabled=1
gpgcheck=0
EOF

sudo dnf clean metadata
dnf repolist --enabled
dnf --disablerepo='*' --enablerepo=rhcsa-custom list rhcsa-toolkit
exit
```

**No bastion, execute:**

```bash
lab grade obj03-05
lab finish obj03-05
```

---

### obj03-06 — Atualizar pacote por repositório de errata

**No bastion, execute:**

```bash
lab start obj03-06
ssh student@servera
```

**No servera, execute:**

```bash
sudo python3 - <<'PY'
from pathlib import Path
p = Path('/etc/yum.repos.d/rhcsa-update.repo')
lines = p.read_text().splitlines()
out = []
section = None
for line in lines:
    if line.startswith('[') and line.endswith(']'):
        section = line[1:-1]
    if section == 'rhcsa-errata' and line.startswith('enabled='):
        line = 'enabled=1'
    out.append(line)
p.write_text('\n'.join(out) + '\n')
PY

sudo dnf -y --disablerepo='*' \
  --enablerepo=rhcsa-base \
  --enablerepo=rhcsa-errata \
  upgrade rhcsa-update-demo

rpm -q rhcsa-update-demo

sudo python3 - <<'PY'
from pathlib import Path
p = Path('/etc/yum.repos.d/rhcsa-update.repo')
lines = p.read_text().splitlines()
p.write_text('\n'.join('enabled=0' if line.startswith('enabled=') else line for line in lines) + '\n')
PY

exit
```

**No bastion, execute:**

```bash
lab grade obj03-06
lab finish obj03-06
```

---

### obj03-07 — Auditar transações com DNF history

**No bastion, execute:**

```bash
lab start obj03-07
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj03-07
sudo dnf -y install rhcsa-history
dnf history list rhcsa-history > output/history-after-install.txt
sudo dnf -y remove rhcsa-history
dnf history list rhcsa-history > output/history-after-remove.txt
id="$(dnf history list rhcsa-history | awk '$1 ~ /^[0-9]+$/ {print $1; exit}')"
dnf history info "$id" > output/last-transaction.txt
exit
```

**No bastion, execute:**

```bash
lab grade obj03-07
lab finish obj03-07
```

---

### obj03-08 — Desafio integrado de gerenciamento de software

**No bastion, execute:**

```bash
lab start obj03-08
ssh student@serverb
```

**No serverb, execute:**

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

sudo dnf -y --disablerepo='*' \
  --enablerepo=rhcsa-system-base \
  install rhcsa-system-1.0-1

rpm -qpi assets/rhcsa-local-1.0-1.noarch.rpm > output/local-rpm-info.txt
sudo dnf -y install ./assets/rhcsa-local-1.0-1.noarch.rpm

sudo python3 - <<'PY'
from pathlib import Path
p = Path('/etc/yum.repos.d/rhcsa-system.repo')
lines = p.read_text().splitlines()
out = []
section = None
for line in lines:
    if line.startswith('[') and line.endswith(']'):
        section = line[1:-1]
    if section == 'rhcsa-system-errata' and line.startswith('enabled='):
        line = 'enabled=1'
    out.append(line)
p.write_text('\n'.join(out) + '\n')
PY

sudo dnf -y --disablerepo='*' \
  --enablerepo=rhcsa-system-base \
  --enablerepo=rhcsa-system-errata \
  upgrade rhcsa-system

rpm -q rhcsa-system rhcsa-local

sudo python3 - <<'PY'
from pathlib import Path
p = Path('/etc/yum.repos.d/rhcsa-system.repo')
lines = p.read_text().splitlines()
p.write_text('\n'.join('enabled=0' if line.startswith('enabled=') else line for line in lines) + '\n')
PY

id="$(dnf history list rhcsa-system | awk '$1 ~ /^[0-9]+$/ {print $1; exit}')"
test -n "$id"
dnf history info "$id" > output/history.txt
exit
```

**No bastion, execute:**

```bash
lab grade obj03-08
lab finish obj03-08
```

---

**Fim do Objective 03 — 8/8 laboratórios.**

> **Uso:** gabarito de consulta/correção. Execute somente nas VMs isoladas do projeto, depois de `lab start`. Os repositórios locais com `gpgcheck=0` pertencem exclusivamente aos cenários didáticos do laboratório.
