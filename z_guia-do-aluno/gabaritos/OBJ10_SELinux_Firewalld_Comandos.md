# RHCSA EX200 v10 — Gabarito Operacional

## Objective 10 — SELinux & firewalld

**Referência:** repositório [`eduardoandradej/rhcsa-ex200-v10-lab`](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab), branch `main` — `prompt.pt.md` e `tests/reference-solutions/obj10-*.sh` dos nove laboratórios.  
**Plataforma local:** RHEL 9.8 • **Referência do exame:** RHEL 10.  
**Execução:** inicie, avalie e finalize no `bastion`; execute a resolução manualmente no `servera` como `student`.  
**Segurança:** não desabilite SELinux nem altere a zona da interface de gerenciamento SSH. As portas e os caminhos deste gabarito são específicos do ambiente `lab start` do repositório.  
**Sequência:** um laboratório por vez; `lab grade` antes de `lab finish`.

---

### obj10-01 — Inventário de SELinux e contextos

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj10-01
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj10-01

getenforce > output/getenforce.txt
sestatus > output/sestatus.txt
ps -eZ | grep '[s]shd' > output/sshd-process.txt
ls -Z /etc/ssh/sshd_config > output/sshd-config.txt
sudo semanage fcontext -l -C > output/fcontext-local.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj10-01
lab finish obj10-01
```

---

### obj10-02 — Restaurar SELinux enforcing atual e persistente

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj10-02
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj10-02

sudo setenforce 1
sudo sed -i 's/^SELINUX=.*/SELINUX=enforcing/' /etc/selinux/config
getenforce > output/getenforce.txt
grep '^SELINUX=' /etc/selinux/config > output/config.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj10-02
lab finish obj10-02
```

---

### obj10-03 — Contexto SELinux persistente com semanage e restorecon

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj10-03
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj10-03

sudo semanage fcontext -a -t httpd_sys_content_t '/srv/web10(/.*)?'
sudo restorecon -Rv /srv/web10
{ ls -Zd /srv/web10; ls -Z /srv/web10/index.html; } > output/contexts.txt
sudo semanage fcontext -l -C | grep '/srv/web10' > output/fcontext.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj10-03
lab finish obj10-03
```

---

### obj10-04 — Boolean SELinux persistente

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj10-04
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj10-04

sudo setsebool -P httpd_enable_homedirs on
getsebool httpd_enable_homedirs > output/getsebool.txt
sudo semanage boolean -l | grep '^httpd_enable_homedirs ' > output/semanage.txt
sudo semanage boolean -l -C > output/custom.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj10-04
lab finish obj10-04
```

---

### obj10-05 — Diagnóstico de AVC e correção de contexto

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj10-05
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj10-05

getenforce
sudo ausearch -if input/avc.audit -m AVC > output/avc.txt
sudo semanage fcontext -a -t httpd_sys_content_t '/srv/avc10(/.*)?'
sudo restorecon -Rv /srv/avc10
ls -Zd /srv/avc10 /srv/avc10/index.html > output/context.txt
curl -sS http://127.0.0.1/avc10/index.html > output/curl.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj10-05
lab finish obj10-05
```

---

### obj10-06 — Zona, origem, serviço e porta no firewalld

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj10-06
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj10-06

sudo firewall-cmd --permanent --zone=rhcsa10 --add-source=198.51.100.0/24
sudo firewall-cmd --permanent --zone=rhcsa10 --add-service=http
sudo firewall-cmd --permanent --zone=rhcsa10 --add-port=45100/tcp
sudo firewall-cmd --reload
sudo firewall-cmd --zone=rhcsa10 --list-all > output/runtime.txt
sudo firewall-cmd --permanent --zone=rhcsa10 --list-all > output/permanent.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj10-06
lab finish obj10-06
```

---

### obj10-07 — Rotular porta não padrão para httpd

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj10-07
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj10-07

sudo semanage port -a -t http_port_t -p tcp 48888
sudo systemctl start httpd
sudo semanage port -l -C > output/ports.txt
sudo ss -ltnp | grep ':48888 ' > output/listen.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj10-07
lab finish obj10-07
```

---

### obj10-08 — Persistência de porta na zona ativa

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj10-08
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj10-08

IFACE=$(ip -o route show default | awk '{print $5; exit}')
ZONE=$(sudo firewall-cmd --get-zone-of-interface="$IFACE")
if [ -z "$ZONE" ] || [ "$ZONE" = "no zone" ]; then ZONE=$(sudo firewall-cmd --get-default-zone); fi
sudo firewall-cmd --permanent --zone="$ZONE" --add-port=45102/tcp
sudo firewall-cmd --reload
printf '%s\n' "$ZONE" > output/zone.txt
sudo firewall-cmd --zone="$ZONE" --query-port=45102/tcp > output/runtime.txt
sudo firewall-cmd --permanent --zone="$ZONE" --query-port=45102/tcp > output/permanent.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj10-08
lab finish obj10-08
```

---

### obj10-09 — Desafio integrado SELinux e firewalld

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj10-09
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj10-09

sudo semanage fcontext -a -t httpd_sys_content_t '/srv/rhcsa10-final(/.*)?'
sudo restorecon -Rv /srv/rhcsa10-final
sudo semanage port -a -t http_port_t -p tcp 48889
IFACE=$(ip -o route show default | awk '{print $5; exit}')
ZONE=$(sudo firewall-cmd --get-zone-of-interface="$IFACE")
if [ -z "$ZONE" ] || [ "$ZONE" = "no zone" ]; then ZONE=$(sudo firewall-cmd --get-default-zone); fi
sudo firewall-cmd --permanent --zone="$ZONE" --add-port=48889/tcp
sudo firewall-cmd --reload
sudo systemctl start httpd
ls -Zd /srv/rhcsa10-final /srv/rhcsa10-final/index.html > output/contexts.txt
sudo semanage port -l -C | grep 48889 > output/selinux-port.txt
printf '%s\n' "$ZONE" > output/zone.txt
sudo firewall-cmd --zone="$ZONE" --query-port=48889/tcp > output/firewall.txt
curl -sS http://127.0.0.1:48889/secure10/index.html > output/curl.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj10-09
lab finish obj10-09
```

---

## Referências e validação

- [Enunciados do OBJ10](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab/tree/main/labs/10-selinux-firewalld)
- [Soluções de referência de QA](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab/tree/main/tests/reference-solutions)

**Escopo da verificação:** comandos transcritos e confrontados com as soluções de referência e os enunciados publicados; blocos Bash verificados sintaticamente. **Não** foram executados nas VMs nesta sessão. Os scripts de referência são usados como base de consulta, não executados no fluxo do aluno.
