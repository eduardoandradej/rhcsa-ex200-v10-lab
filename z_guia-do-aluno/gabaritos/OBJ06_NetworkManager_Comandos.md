# RHCSA EX200 v10 — Gabarito Operacional

## Objective 06 — NetworkManager, IP Networking & Name Resolution

**Referência:** repositório [`eduardoandradej/rhcsa-ex200-v10-lab`](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab), branch `main` — enunciados `prompt.pt.md`, scripts `tests/reference-solutions/obj06-*.sh` e graders do Objective 06.  
**Plataforma local:** RHEL 9.8 • **Referência do exame:** RHEL 10.  
**Execução:** execute `lab start`, `lab grade` e `lab finish` no `bastion`. Execute os comandos como `student` no nó indicado.  
**Atenção:** os perfis do exercício utilizam a interface isolada `ex200a`. **Não altere a interface de gerenciamento/SSH.**  
**Sequência:** execute um laboratório por vez; confirme o resultado de `lab grade` antes de `lab finish`.

---

### obj06-01 — Inventariar dispositivos e conexões de rede

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj06-01
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj06-01

nmcli device status > output/devices.txt
nmcli connection show > output/connections.txt
nmcli connection show --active > output/active.txt
ip -br link show ex200a > output/ex200a-link.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj06-01
lab finish obj06-01
```

---

### obj06-02 — Criar perfil IPv4 estático com nmcli

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj06-02
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj06-02

sudo nmcli connection add \
  con-name ex200-static \
  type ethernet \
  ifname ex200a \
  ipv4.method manual \
  ipv4.addresses 10.66.2.10/24 \
  ipv6.method disabled \
  connection.autoconnect yes

sudo nmcli connection up ex200-static

ping -c 2 10.66.2.254 > output/ping.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj06-02
lab finish obj06-02
```

---

### obj06-03 — Modificar perfil, gateway e IPv4 secundário

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj06-03
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj06-03

sudo nmcli connection modify ex200-mod \
  ipv4.addresses 10.66.3.20/24 \
  +ipv4.addresses 10.66.3.120/24 \
  ipv4.never-default yes \
  connection.autoconnect yes

sudo nmcli connection modify ex200-mod ipv4.gateway ""

sudo nmcli connection up ex200-mod

nmcli -f connection.id,connection.autoconnect,ipv4.method,ipv4.addresses,ipv4.gateway,ipv4.never-default \
  connection show ex200-mod > output/profile.txt

ip -4 -br addr show ex200a > output/runtime.txt
ping -c 2 10.66.3.254 > output/ping.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj06-03
lab finish obj06-03
```

---

### obj06-04 — Configurar perfil dual-stack IPv4 e IPv6

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj06-04
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj06-04

sudo nmcli connection add \
  con-name ex200-dual \
  type ethernet \
  ifname ex200a \
  ipv4.method manual \
  ipv4.addresses 10.66.4.10/24 \
  ipv6.method manual \
  ipv6.addresses fd00:66:4::10/64 \
  connection.autoconnect yes

sudo nmcli connection up ex200-dual

ping -c 2 10.66.4.254 > output/ping4.txt
ping -6 -c 2 fd00:66:4::fe > output/ping6.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj06-04
lab finish obj06-04
```

---

### obj06-05 — Editar perfil NetworkManager em formato keyfile

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj06-05
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj06-05

sudo python3 - <<'PY'
from pathlib import Path

path = Path('/etc/NetworkManager/system-connections/ex200-keyfile.nmconnection')
content = path.read_text()
if '10.66.5.110/24' not in content:
    content = content.replace(
        'address1=10.66.5.10/24',
        'address1=10.66.5.10/24\naddress2=10.66.5.110/24'
    )
path.write_text(content)
PY

sudo nmcli connection reload
sudo nmcli connection up ex200-keyfile

ip -4 -br addr show ex200a > output/runtime.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj06-05
lab finish obj06-05
```

---

### obj06-06 — Configurar hostname e resolução local

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj06-06
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj06-06

sudo hostname temporary-net
hostname > output/temporary-hostname.txt
cat /etc/hostname > output/static-before.txt

sudo hostnamectl set-hostname nodea.lab.test

printf '%s\n' '10.66.6.254 peer06.lab.test peer06' | \
  sudo tee -a /etc/hosts > /dev/null

getent hosts peer06 > output/getent.txt
ping -c 2 peer06 > output/ping.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj06-06
lab finish obj06-06
```

---

### obj06-07 — Configurar DNS e search domain em perfil NetworkManager

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj06-07
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj06-07

sudo nmcli connection modify ex200-dns \
  ipv4.dns "192.0.2.53 192.0.2.54" \
  ipv4.dns-search lab.example \
  ipv4.ignore-auto-dns yes \
  ipv4.never-default yes \
  connection.autoconnect no

nmcli -f ipv4.dns,ipv4.dns-search,ipv4.ignore-auto-dns,ipv4.never-default,connection.autoconnect \
  connection show ex200-dns > output/dns-profile.txt

grep '^hosts:' /etc/nsswitch.conf > output/nsswitch-hosts.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj06-07
lab finish obj06-07
```

---

### obj06-08 — Desafio integrado de NetworkManager e resolução

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj06-08
ssh student@serverb
```

**No serverb, execute:**

```bash
cd /home/student/rhcsa-lab/obj06-08

sudo nmcli connection add \
  con-name exam-net \
  type ethernet \
  ifname ex200a \
  ipv4.method manual \
  ipv4.addresses 10.66.8.20/24 \
  ipv6.method manual \
  ipv6.addresses fd00:66:8::20/64 \
  connection.autoconnect yes

sudo nmcli connection modify exam-net \
  +ipv4.addresses 10.66.8.120/24

sudo nmcli connection up exam-net

sudo hostnamectl set-hostname serverb-net.lab.test

printf '%s\n' '10.66.8.254 peer-net.lab.test peer-net' | \
  sudo tee -a /etc/hosts > /dev/null

nmcli -f connection.id,connection.interface-name,connection.autoconnect,ipv4.method,ipv4.addresses,ipv6.method,ipv6.addresses \
  connection show exam-net > output/profile.txt

ip -br addr show ex200a > output/runtime.txt
ping -c 2 10.66.8.254 > output/ping4.txt
ping -6 -c 2 fd00:66:8::fe > output/ping6.txt
getent hosts peer-net > output/getent.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj06-08
lab finish obj06-08
```

---

## Referências de consulta

- [Enunciados — Objective 06](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab/tree/main/labs/06-networking)
- [Soluções de referência — obj06-01 a obj06-08](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab/tree/main/tests/reference-solutions)

**Validação:** conteúdo confrontado com os enunciados, scripts de referência e critérios dos graders publicados na branch `main` em 12/10/2026. A sintaxe dos blocos Bash foi verificada; **não houve execução dos laboratórios nem confirmação de pontuação nas VMs nesta sessão**.
