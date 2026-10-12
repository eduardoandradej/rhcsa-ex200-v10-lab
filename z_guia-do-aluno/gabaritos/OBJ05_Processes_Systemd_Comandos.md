# RHCSA EX200 v10 — Gabarito Operacional

## Objective 05 — Processes, Scheduling, Tuning & systemd

**Referência:** repositório [`eduardoandradej/rhcsa-ex200-v10-lab`](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab), branch `main` — enunciados `prompt.pt.md`, scripts `tests/reference-solutions/obj05-*.sh` e graders do Objective 05.  
**Plataforma local:** RHEL 9.8 • **Referência do exame:** RHEL 10.  
**Execução:** use `lab start`, `lab grade` e `lab finish` no `bastion`. Execute os comandos como `student` no nó indicado, utilizando `sudo` apenas onde necessário.  
**Sequência:** um laboratório ativo por vez; confira o `lab grade` antes de executar `lab finish`.

---

### obj05-01 — Identificar processos, PIDs e estados

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj05-01
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj05-01

ps -o pid=,ppid=,stat=,ni=,args= \
  -p "$(cat /run/rhcsa-proc-sleeper.pid)" > output/sleeper.txt

ps -o pid=,ppid=,stat=,ni=,args= \
  -p "$(cat /run/rhcsa-proc-stopped.pid)" > output/stopped.txt

cat output/sleeper.txt
cat output/stopped.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj05-01
lab finish obj05-01
```

---

### obj05-02 — Controlar jobs em foreground e background

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj05-02
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj05-02
set -m

nohup ./assets/job-alpha >/dev/null 2>&1 &
alpha=$!
echo "$alpha" > output/alpha.pid

nohup ./assets/job-beta >/dev/null 2>&1 &
beta=$!
echo "$beta" > output/beta.pid

for _ in {1..100}; do
    a_args="$(ps -o args= -p "$alpha" 2>/dev/null || true)"
    b_args="$(ps -o args= -p "$beta" 2>/dev/null || true)"
    [[ "$a_args" == rhcsa-job-alpha* && "$b_args" == rhcsa-job-beta* ]] && break
    sleep 0.02
done

kill -s STOP %1

for _ in {1..50}; do
    state="$(ps -o stat= -p "$alpha" 2>/dev/null || true)"
    [[ "$state" == *T* ]] && break
    sleep 0.02
done

jobs -l > output/jobs.txt
ps -o pid=,stat=,args= -p "$alpha,$beta" > output/processes.txt

kill -s CONT %1
disown %1 %2

exit
```

**No bastion, execute:**

```bash
ssh student@servera 'kill -s STOP "$(cat /home/student/rhcsa-lab/obj05-02/output/alpha.pid)"'

lab grade obj05-02
lab finish obj05-02
```

---

### obj05-03 — Controlar processos com sinais

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj05-03
ssh student@servera
```

**No servera, execute:**

```bash
kill -s STOP "$(cat /run/rhcsa-signal-alpha.pid)"
kill -s TERM "$(cat /run/rhcsa-signal-beta.pid)"
kill -s CONT "$(cat /run/rhcsa-signal-gamma.pid)"

sleep 0.2

ps -o pid=,stat=,args= -p "$(cat /run/rhcsa-signal-alpha.pid)"
ps -o pid=,stat=,args= -p "$(cat /run/rhcsa-signal-gamma.pid)"

exit
```

**No bastion, execute:**

```bash
lab grade obj05-03
lab finish obj05-03
```

---

### obj05-04 — Identificar e encerrar processos intensivos

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj05-04
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj05-04

cpid="$(cat /run/rhcsa-cpu-hog.pid)"
mpid="$(cat /run/rhcsa-mem-hog.pid)"

ps -o pid=,%cpu=,%mem=,stat=,args= -p "$cpid" > output/cpu-before.txt
ps -o pid=,%cpu=,%mem=,stat=,args= -p "$mpid" > output/memory-before.txt

kill -s TERM "$cpid"
kill -s TERM "$mpid"

for _ in {1..30}; do
    [[ ! -e "/proc/$cpid" && ! -e "/proc/$mpid" ]] && break
    sleep 0.1
done

exit
```

**No bastion, execute:**

```bash
lab grade obj05-04
lab finish obj05-04
```

---

### obj05-05 — Ajustar prioridade com nice e renice

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj05-05
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj05-05

nohup nice -n 12 ./assets/nice-start >/dev/null 2>&1 &
p1=$!
echo "$p1" > output/nice-start.pid

nohup ./assets/nice-change >/dev/null 2>&1 &
p2=$!
echo "$p2" > output/nice-change.pid

for _ in {1..100}; do
    a1="$(ps -o args= -p "$p1" 2>/dev/null || true)"
    a2="$(ps -o args= -p "$p2" 2>/dev/null || true)"
    [[ "$a1" == rhcsa-nice-start* && "$a2" == rhcsa-nice-change* ]] && break
    sleep 0.02
done

renice -n 7 -p "$p2"

ps -o pid=,ni=,stat=,args= -p "$p1,$p2" > output/priorities.txt

disown -a 2>/dev/null || true

exit
```

**No bastion, execute:**

```bash
lab grade obj05-05
lab finish obj05-05
```

---

### obj05-06 — Gerenciar perfis de ajuste com TuneD

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj05-06
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj05-06

tuned-adm recommend > output/recommended.txt
tuned-adm list > output/profiles.txt

sudo tuned-adm profile throughput-performance

tuned-adm active > output/active.txt

sudo tuned-adm verify > output/verify.txt 2>&1
printf '%s\n' "$?" > output/verify.rc

tuned-adm active

exit
```

**No bastion, execute:**

```bash
lab grade obj05-06
lab finish obj05-06
```

---

### obj05-07 — Identificar units e estados do systemd

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj05-07
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj05-07

systemctl list-units --type=service --all --no-pager > output/services.txt
systemctl list-unit-files --type=service --no-pager > output/unit-files.txt
systemctl is-active sshd.service > output/sshd-active.txt
systemctl is-enabled sshd.service > output/sshd-enabled.txt
systemctl status chronyd.service --no-pager > output/chronyd-status.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj05-07
lab finish obj05-07
```

---

### obj05-08 — Start, restart e reload de serviço

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj05-08
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj05-08

sudo systemctl start rhcsa-control.service
systemctl show -p MainPID --value rhcsa-control.service > output/start.pid

sudo systemctl restart rhcsa-control.service
systemctl show -p MainPID --value rhcsa-control.service > output/restart.pid

sudo systemctl reload rhcsa-control.service
systemctl show -p MainPID --value rhcsa-control.service > output/reload.pid

exit
```

**No bastion, execute:**

```bash
lab grade obj05-08
lab finish obj05-08
```

---

### obj05-09 — Enable, disable, mask e dependências

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj05-09
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj05-09

sudo systemctl enable --now rhcsa-boot.service

systemctl list-dependencies rhcsa-boot.service --no-pager \
  > output/boot-dependencies.txt

sudo systemctl stop rhcsa-blocked.service
sudo systemctl disable rhcsa-blocked.service
sudo systemctl mask rhcsa-blocked.service

exit
```

**No bastion, execute:**

```bash
lab grade obj05-09
lab finish obj05-09
```

---

### obj05-10 — Desafio integrado de processos e systemd

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj05-10
ssh student@serverb
```

**No serverb, execute:**

```bash
cd /home/student/rhcsa-lab/obj05-10

rogue="$(cat /run/rhcsa-rogue-cpu.pid)"

ps -o pid=,%cpu=,%mem=,ni=,stat=,args= -p "$rogue" \
  > output/rogue-before.txt

kill -s TERM "$rogue"

for _ in {1..30}; do
    [[ ! -e "/proc/$rogue" ]] && break
    sleep 0.1
done

nohup nice -n 10 ./assets/batch-worker >/dev/null 2>&1 &
batch=$!
echo "$batch" > output/batch.pid

for _ in {1..100}; do
    args="$(ps -o args= -p "$batch" 2>/dev/null || true)"
    [[ "$args" == rhcsa-batch-worker* ]] && break
    sleep 0.02
done

disown -a 2>/dev/null || true

sudo systemctl enable --now rhcsa-api.service

sudo systemctl stop rhcsa-legacy.service
sudo systemctl disable rhcsa-legacy.service
sudo systemctl mask rhcsa-legacy.service

sudo tuned-adm profile balanced

tuned-adm active > output/tuned-active.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj05-10
lab finish obj05-10
```

---

## Referências de consulta

- [Enunciados — Objective 05](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab/tree/main/labs/05-processes-systemd)
- [Soluções de referência da engenharia (obj05-01 a obj05-10)](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab/tree/main/tests/reference-solutions)

**Validação:** comandos estruturados a partir dos enunciados e das soluções de referência da branch `main`. A sintaxe dos blocos Bash foi verificada; a execução real dos graders nas VMs não foi realizada nesta sessão.
