# RHCSA EX200 v10 — Gabarito Operacional

## Objective 11 — NFS & AutoFS

**Referência:** repositório [`eduardoandradej/rhcsa-ex200-v10-lab`](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab), branch `main` — enunciados `prompt.pt.md`, arquivos `solution.md`, scripts `tests/reference-solutions/obj11-*.sh` e critérios `grade.py` dos seis laboratórios.  
**Plataforma local:** RHEL 9.8 • **Referência do exame:** RHEL 10.  
**Execução:** inicie, avalie e finalize no `bastion`; execute a resolução manualmente no `servera` como `student`. O `serverb` fornece os exports NFS preparados pelo `lab start`, sem comandos manuais adicionais neste objetivo.  
**Sequência:** um laboratório de cada vez; execute `lab grade` antes de `lab finish`.  
**Segurança:** utilize somente a rede e os diretórios do laboratório. Não modifique exports NFS ou arquivos do sistema fora do escopo do exercício.

---

### obj11-01 — Descobrir, montar e desmontar NFS

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj11-01
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj11-01

showmount --exports serverb > output/exports.txt
sudo mount -t nfs -o rw,sync serverb:/srv/rhcsa11/manual /mnt/rhcsa11-manual
findmnt /mnt/rhcsa11-manual > output/mount.txt
cat /mnt/rhcsa11-manual/hello.txt > output/content.txt
sudo umount /mnt/rhcsa11-manual

if findmnt /mnt/rhcsa11-manual >/dev/null 2>&1; then
  echo mounted > output/unmounted.txt
else
  echo unmounted > output/unmounted.txt
fi

exit
```

**No bastion, execute:**

```bash
lab grade obj11-01
lab finish obj11-01
```

---

### obj11-02 — Montagem NFS persistente no fstab

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj11-02
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj11-02

echo 'serverb:/srv/rhcsa11/persist /mnt/rhcsa11-persist nfs rw,sync 0 0' | \
  sudo tee -a /etc/fstab >/dev/null

sudo systemctl daemon-reload
sudo mount /mnt/rhcsa11-persist
findmnt /mnt/rhcsa11-persist > output/findmnt.txt
sudo findmnt --verify > output/verify.txt 2>&1
cat /mnt/rhcsa11-persist/hello.txt > output/content.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj11-02
lab finish obj11-02
```

---

### obj11-03 — Mapa direto do AutoFS

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj11-03
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj11-03

echo '/- /etc/auto.rhcsa11' | \
  sudo tee /etc/auto.master.d/rhcsa11.autofs >/dev/null

echo '/home/student/direct11 -fstype=nfs,rw,sync serverb:/srv/rhcsa11/direct' | \
  sudo tee /etc/auto.rhcsa11 >/dev/null

sudo systemctl enable --now autofs
cat /home/student/direct11/hello.txt > output/content.txt
findmnt -T /home/student/direct11/hello.txt > output/findmnt.txt
systemctl is-active autofs > output/service.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj11-03
lab finish obj11-03
```

---

### obj11-04 — Mapa indireto com wildcard no AutoFS

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj11-04
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj11-04

echo '/remote11 /etc/auto.rhcsa11' | \
  sudo tee /etc/auto.master.d/rhcsa11.autofs >/dev/null

echo '* -rw,sync,fstype=nfs serverb:/srv/rhcsa11/projects/&' | \
  sudo tee /etc/auto.rhcsa11 >/dev/null

sudo systemctl enable --now autofs

{
  cat /remote11/alpha/info.txt
  cat /remote11/beta/info.txt
} > output/content.txt

{
  findmnt -T /remote11/alpha/info.txt
  findmnt -T /remote11/beta/info.txt
} > output/findmnt.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj11-04
lab finish obj11-04
```

---

### obj11-05 — Automount NFS via systemd e fstab

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj11-05
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj11-05

echo 'serverb:/srv/rhcsa11/systemd /mnt/rhcsa11-auto nfs rw,sync,x-systemd.automount 0 0' | \
  sudo tee -a /etc/fstab >/dev/null

sudo systemctl daemon-reload
UNIT=$(systemd-escape --path --suffix=automount /mnt/rhcsa11-auto)
sudo systemctl start "$UNIT"
systemctl is-active "$UNIT" > output/unit.txt
cat /mnt/rhcsa11-auto/hello.txt > output/content.txt
findmnt -T /mnt/rhcsa11-auto/hello.txt > output/findmnt.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj11-05
lab finish obj11-05
```

---

### obj11-06 — Desafio integrado NFS e AutoFS

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj11-06
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj11-06

sudo mount -t nfs -o rw,sync serverb:/srv/rhcsa11/integrated /mnt/rhcsa11-check
findmnt /mnt/rhcsa11-check > output/manual.txt
ls -l /mnt/rhcsa11-check > output/list.txt
sudo umount /mnt/rhcsa11-check

echo '/remote11-final /etc/auto.rhcsa11' | \
  sudo tee /etc/auto.master.d/rhcsa11.autofs >/dev/null

echo '* -rw,sync,fstype=nfs serverb:/srv/rhcsa11/integrated/&' | \
  sudo tee /etc/auto.rhcsa11 >/dev/null

sudo systemctl enable --now autofs

{
  cat /remote11-final/red/info.txt
  cat /remote11-final/hat/info.txt
} > output/content.txt

{
  findmnt -T /remote11-final/red/info.txt
  findmnt -T /remote11-final/hat/info.txt
} > output/findmnt.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj11-06
lab finish obj11-06
```

---

## Consulta rápida

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab status
lab list --objective obj11
lab show obj11-01
```

**Para executar um laboratório específico:**

```bash
lab start obj11-01
ssh student@servera
```

**Após resolver e sair do servera:**

```bash
lab grade obj11-01
lab finish obj11-01
lab status
```

---

**Fontes:** [laboratórios do Objective 11](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab/tree/main/labs/11-nfs-autofs) · [scripts de referência de QA](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab/tree/main/tests/reference-solutions).  
**Nota:** os blocos foram conferidos com os comandos de referência e os requisitos observados pelos graders. A sintaxe Bash foi validada; a execução real e a pontuação `lab grade` ainda devem ser confirmadas nas VMs do projeto.
