# RHCSA EX200 v10 — Gabarito Operacional

## Objective 01 — Essential Tools

**Referência:** repositório `eduardoandradej/rhcsa-ex200-v10-lab`, branch `main`.  
**Plataforma do laboratório:** RHEL 9.8 • **Alvo de estudos:** RHEL 10.  
**Convenção:** execute as seções de cada laboratório na ordem apresentada; `lab start`, `lab grade` e `lab finish` são executados no `bastion`. As operações nos nós são executadas como `student`, exceto quando indicado.

---

### obj01-01 — Operações com arquivos

**No bastion, execute:**
```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj01-01
ssh student@servera
```

**No servera, execute:**
```bash
cd /home/student/rhcsa-lab/obj01-01
mkdir -p workspace/{reports,images,notes}
cp input/report-*.txt workspace/reports/
mv input/image-*.jpg workspace/images/
mv input/notes-old.txt workspace/notes/notes-final.txt
touch workspace/notes/note-{1..3}.txt
rm input/*.tmp
exit
```

**No bastion, execute:**
```bash
lab grade obj01-01
lab finish obj01-01
```

---

### obj01-02 — Redirecionamento e pipes

**No bastion, execute:**
```bash
lab start obj01-02
ssh student@servera
```

**No servera, execute:**
```bash
cd /home/student/rhcsa-lab/obj01-02
bin/stream-demo > output/stdout.log 2> output/stderr.log
bin/stream-demo > output/combined.log 2>&1
bin/append-demo >> output/append.log
bin/append-demo >> output/append.log
sort input/services.txt | uniq > output/services-unique.txt
grep -w 'active' input/status.txt | wc -l > output/active-count.txt
exit
```

**No bastion, execute:**
```bash
lab grade obj01-02
lab finish obj01-02
```

---

### obj01-03 — grep e expressões regulares

**No bastion, execute:**
```bash
lab start obj01-03
ssh student@servera
```

**No servera, execute:**
```bash
cd /home/student/rhcsa-lab/obj01-03
grep -E '^SRV-[0-9]{3}\|' input/systems.txt > output/servers.txt
grep -E '\|web[^|]*\|' input/systems.txt > output/web-hosts.txt
grep -F '|prod|active|' input/systems.txt > output/prod-active.txt
grep -E 'WARN|ERROR' input/events.log > output/alerts.log
grep -E '\.21$' input/systems.txt > output/ip-ending-21.txt
exit
```

**No bastion, execute:**
```bash
lab grade obj01-03
lab finish obj01-03
```

---

### obj01-04 — SSH e troca de usuários

**No bastion, execute:**
```bash
lab start obj01-04
ssh student@servera
```

**No servera (student), execute:**
```bash
cd /home/student/rhcsa-lab/obj01-04
ssh student@serverb 'hostname -f' > remote-host.txt
ssh student@serverb 'whoami' > remote-user.txt
su - labuser
```

**No servera (labuser), execute:**
```bash
whoami > /home/labuser/switch-user.txt
exit
```

**No servera (student), execute:**
```bash
exit
```

**No bastion, execute:**
```bash
lab grade obj01-04
lab finish obj01-04
```

> Senha didática solicitada pelo `su - labuser`: `redhat`.

---

### obj01-05 — Arquivos e compressão

**No bastion, execute:**
```bash
lab start obj01-05
ssh student@servera
```

**No servera, execute:**
```bash
cd /home/student/rhcsa-lab/obj01-05
tar -cf output/project.tar project
gzip -c output/project.tar > output/project.tar.gz
bzip2 -c output/project.tar > output/project.tar.bz2
tar -xzf output/project.tar.gz -C restore-gzip
tar -xjf output/project.tar.bz2 -C restore-bzip2
exit
```

**No bastion, execute:**
```bash
lab grade obj01-05
lab finish obj01-05
```

---

### obj01-06 — Edição de arquivos de texto com Vim

**No bastion, execute:**
```bash
lab start obj01-06
ssh student@servera
```

**No servera, execute:**
```bash
cd /home/student/rhcsa-lab/obj01-06
vim app.conf
```

**Dentro do Vim (`app.conf`), execute as linhas de comando:**
```vim
:%s/^environment=development$/environment=production/
:%s/^workers=2$/workers=8/
:g/^debug=true$/d
:g/^workers=8$/s/$/\rlogging=verbose/
:wq
```

**No servera, execute:**
```bash
vim notes.txt
```

**Dentro do Vim (`notes.txt`):** pressione `i`, digite as três linhas abaixo, pressione `Esc` e execute `:wq`.
```text
review completed
configuration updated
ready for validation
```

**No servera, execute:**
```bash
exit
```

**No bastion, execute:**
```bash
lab grade obj01-06
lab finish obj01-06
```

---

### obj01-07 — Hard links e symbolic links

**No bastion, execute:**
```bash
lab start obj01-07
ssh student@servera
```

**No servera, execute:**
```bash
cd /home/student/rhcsa-lab/obj01-07
ln data/inventory.txt links/inventory.hard
ln -s ../data/app.conf links/current.conf
ln -s ../data/docs links/docs
exit
```

**No bastion, execute:**
```bash
lab grade obj01-07
lab finish obj01-07
```

---

### obj01-08 — Permissões de arquivos

**No bastion, execute:**
```bash
lab start obj01-08
ssh student@servera
```

**No servera, execute:**
```bash
cd /home/student/rhcsa-lab/obj01-08
chmod 640 data/report.txt
chmod 750 data/scripts
chmod u+x data/scripts/backup.sh
umask 0027
touch generated/new-file.txt
mkdir generated/new-dir
exit
```

**No bastion, execute:**
```bash
lab grade obj01-08
lab finish obj01-08
```

---

### obj01-09 — Documentação do sistema

**No bastion, execute:**
```bash
lab start obj01-09
ssh student@servera
```

**No servera, execute:**
```bash
cd /home/student/rhcsa-lab/obj01-09
man -w chmod > output/chmod-manpath.txt
printf '1\n' > output/chmod-section.txt
printf '5\n' > output/passwd-section.txt
rpm -qd openssh-clients | grep -E '/ssh\.1(\.gz)?$' > output/ssh-manpage.txt
printf '%s\n' '-c' > output/tar-create-option.txt
exit
```

**No bastion, execute:**
```bash
lab grade obj01-09
lab finish obj01-09
```

---

### obj01-10 — Desafio integrado Essential Tools

**No bastion, execute:**
```bash
lab start obj01-10
ssh student@servera
```

**No servera, execute:**
```bash
cd /home/student/rhcsa-lab/obj01-10
mkdir -p work/{reports,logs,links,archive}
cp input/report.txt work/reports/final-report.txt
grep -F '|prod|active|' input/systems.txt > work/reports/prod-active.txt
grep -E 'WARN|ERROR' input/events.log > work/logs/alerts.log
ssh student@serverb 'hostname -f' > work/reports/remote-host.txt
sed -i 's/STATUS=PENDING/STATUS=READY/' work/reports/final-report.txt
chmod 640 work/reports/final-report.txt
chmod 750 work/reports
ln work/reports/final-report.txt work/links/report.hard
ln -s ../logs/alerts.log work/links/alerts.current
(
  cd work
  tar -czf archive/evidence.tar.gz reports logs
)
man -w chmod > work/reports/chmod-manpath.txt
exit
```

**No bastion, execute:**
```bash
lab grade obj01-10
lab finish obj01-10
```

---

**Fontes verificadas:** `labs/01-essential-tools/*/prompt.pt.md` e `labs/01-essential-tools/*/solution.md` da branch pública `main`. O documento é um gabarito de consulta e deve permanecer separado da documentação destinada a estudantes que queiram resolver os desafios sem respostas. **Não foi executado contra as VMs nesta sessão.**
