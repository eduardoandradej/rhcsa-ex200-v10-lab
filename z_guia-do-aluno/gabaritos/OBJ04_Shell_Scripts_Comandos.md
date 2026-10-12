# RHCSA EX200 v10 — Gabarito Operacional

## Objective 04 — Simple Shell Scripts

**Referência:** repositório [`eduardoandradej/rhcsa-ex200-v10-lab`](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab), branch `main` — enunciados `prompt.pt.md`, scripts `tests/reference-solutions/obj04-*.sh` e graders do Objective 04.  
**Plataforma local:** RHEL 9.8 • **Referência do exame:** RHEL 10.  
**Execução:** use `lab start`, `lab grade` e `lab finish` no `bastion`. Crie e execute os scripts como `student` no nó indicado.  
**Sequência:** trabalhe em um laboratório por vez. Execute `lab finish` somente depois de conferir a avaliação.

---

### obj04-01 — Parâmetros posicionais e validação de entrada

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj04-01
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj04-01

cat > greet.sh <<'EOF'
#!/bin/bash
if [ "$#" -ne 2 ]; then
    echo "Usage: greet.sh USER ROLE" >&2
    exit 2
fi
echo "USER=$1 ROLE=$2"
EOF

chmod +x greet.sh
bash -n greet.sh
./greet.sh alice admin
./greet.sh bob operations

exit
```

**No bastion, execute:**

```bash
lab grade obj04-01
lab finish obj04-01
```

---

### obj04-02 — Condições com test e colchetes

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj04-02
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj04-02

cat > checkpath.sh <<'EOF'
#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Usage: checkpath.sh PATH" >&2
    exit 2
fi
if [ -f "$1" ]; then
    echo "FILE:$1"
elif [ -d "$1" ]; then
    echo "DIRECTORY:$1"
else
    echo "MISSING:$1"
    exit 1
fi
EOF

chmod +x checkpath.sh
bash -n checkpath.sh
./checkpath.sh /etc/passwd
./checkpath.sh /etc

exit
```

**No bastion, execute:**

```bash
lab grade obj04-02
lab finish obj04-02
```

---

### obj04-03 — Decisões a partir do status de comandos

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj04-03
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj04-03

cat > checkcmd.sh <<'EOF'
#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Usage: checkcmd.sh COMMAND" >&2
    exit 2
fi
if path=$(command -v "$1"); then
    echo "FOUND:$1:$path"
else
    echo "NOTFOUND:$1"
    exit 1
fi
EOF

chmod +x checkcmd.sh
bash -n checkcmd.sh
./checkcmd.sh bash
./checkcmd.sh hostname

exit
```

**No bastion, execute:**

```bash
lab grade obj04-03
lab finish obj04-03
```

---

### obj04-04 — Processar saída de comandos em um script

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj04-04
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj04-04

cat > sysreport.sh <<'EOF'
#!/bin/bash
host=$(hostname -s)
kernel=$(uname -r)
bash_path=$(command -v bash)
user_count=$(getent passwd | wc -l)
echo "HOSTNAME=$host"
echo "KERNEL=$kernel"
echo "BASH_PATH=$bash_path"
echo "USER_COUNT=$user_count"
EOF

chmod +x sysreport.sh
bash -n sysreport.sh
./sysreport.sh

exit
```

**No bastion, execute:**

```bash
lab grade obj04-04
lab finish obj04-04
```

---

### obj04-05 — Loop sobre argumentos da linha de comando

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj04-05
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj04-05

cat > argloop.sh <<'EOF'
#!/bin/bash
if [ "$#" -eq 0 ]; then
    echo "NO-ARGS"
    exit 1
fi
for item in "$@"; do
    echo "ARG:$item"
done
EOF

chmod +x argloop.sh
bash -n argloop.sh
./argloop.sh alpha "beta gamma" delta

exit
```

**No bastion, execute:**

```bash
lab grade obj04-05
lab finish obj04-05
```

---

### obj04-06 — Loop sobre entrada de arquivo

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj04-06
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj04-06

cat > fileloop.sh <<'EOF'
#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Usage: fileloop.sh FILE" >&2
    exit 2
fi
if [ ! -f "$1" ]; then
    echo "MISSING-FILE:$1"
    exit 1
fi
for item in $(cat "$1"); do
    [ -n "$item" ] && echo "ITEM:$item"
done
EOF

chmod +x fileloop.sh
bash -n fileloop.sh
./fileloop.sh assets/services.list

exit
```

**No bastion, execute:**

```bash
lab grade obj04-06
lab finish obj04-06
```

---

### obj04-07 — Relatório de usuários com loop e saída de comandos

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj04-07
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj04-07

cat > userreport.sh <<'EOF'
#!/bin/bash
if [ "$#" -eq 0 ]; then
    echo "NO-USERS"
    exit 1
fi
for user in "$@"; do
    if entry=$(getent passwd "$user"); then
        uid=$(echo "$entry" | cut -d: -f3)
        home=$(echo "$entry" | cut -d: -f6)
        shell=$(echo "$entry" | cut -d: -f7)
        echo "USER:$user:UID=$uid:HOME=$home:SHELL=$shell"
    else
        echo "USER:$user:MISSING"
    fi
done
EOF

chmod +x userreport.sh
bash -n userreport.sh
./userreport.sh root student rhcsa-missing-user

exit
```

**No bastion, execute:**

```bash
lab grade obj04-07
lab finish obj04-07
```

---

### obj04-08 — Desafio integrado de shell scripting

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj04-08
ssh student@serverb
```

**No serverb, execute:**

```bash
cd /home/student/rhcsa-lab/obj04-08

cat > account-audit.sh <<'EOF'
#!/bin/bash
if [ "$#" -ne 2 ]; then
    echo "Usage: account-audit.sh INPUT_FILE OUTPUT_FILE" >&2
    exit 2
fi

input=$1
output=$2

if [ ! -f "$input" ]; then
    echo "MISSING-FILE:$input"
    exit 1
fi

host=$(hostname -s)
total=0
found=0
missing=0

echo "HOST=$host" > "$output"
for user in $(cat "$input"); do
    [ -z "$user" ] && continue
    total=$(( total + 1 ))

    if entry=$(getent passwd "$user"); then
        uid=$(echo "$entry" | cut -d: -f3)

        if [ "$uid" -eq 0 ]; then
            type=PRIVILEGED
        elif [ "$uid" -lt 1000 ]; then
            type=SYSTEM
        else
            type=REGULAR
        fi
        echo "USER:$user:UID=$uid:TYPE=$type" >> "$output"
        found=$(( found + 1 ))
    else
        echo "USER:$user:MISSING" >> "$output"
        missing=$(( missing + 1 ))
    fi
done

echo "SUMMARY:TOTAL=$total:FOUND=$found:MISSING=$missing" >> "$output"
EOF

chmod +x account-audit.sh
bash -n account-audit.sh
./account-audit.sh assets/users.list output/report.txt
cat output/report.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj04-08
lab finish obj04-08
```

---

## Fechamento do Objective 04

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab status
lab list --objective obj04
```

**Próximo objetivo:** OBJ05 — Processes, Scheduling, Tuning & systemd.

**Observação:** os comandos seguem as soluções de referência de QA do projeto. O teste de sintaxe Bash foi realizado localmente; `lab grade` deve ser executado nas VMs do laboratório para confirmar a pontuação.
