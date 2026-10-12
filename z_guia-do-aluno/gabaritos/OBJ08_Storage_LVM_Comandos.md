# RHCSA EX200 v10 — Gabarito Operacional

## Objective 08 — Partitions, Filesystems, Swap & LVM

**Referência:** repositório [`eduardoandradej/rhcsa-ex200-v10-lab`](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab), branch `main` — enunciados `prompt.pt.md`, scripts `tests/reference-solutions/obj08-*.sh` e grader de cada laboratório.  
**Plataforma local:** RHEL 9.8 • **Referência do exame:** RHEL 10.  
**Execução:** inicie, avalie e finalize no `bastion`; execute os comandos como `student` no `servera`.  
**Segurança:** execute apenas depois de `lab start` concluir com sucesso e de validar os discos na VM do laboratório. Os dispositivos `/dev/vdb`, `/dev/vdc`, `/dev/vdd` e `/dev/vde` são discos scratch **somente na topologia prevista do projeto**. Nunca execute comandos destrutivos no `/dev/vda` ou em discos de produção. Preserve o swap original.  
**Sequência:** um lab por vez, `lab grade` e somente depois `lab finish`.

---

### obj08-01 — Inventariar dispositivos de bloco

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj08-01
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj08-01

lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,UUID > output/lsblk.txt
sudo blkid > output/blkid.txt
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdb print > output/parted-vdb.txt 2>&1 || true
sudo pvs > output/pvs.txt
sudo vgs > output/vgs.txt
sudo lvs > output/lvs.txt
findmnt > output/findmnt.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj08-01
lab finish obj08-01
```

---

### obj08-02 — Criar GPT e partição

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj08-02
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj08-02

sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdb mklabel gpt
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdb mkpart data08 xfs 1MiB 1025MiB
sudo udevadm settle --timeout=15
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdb unit MiB print > output/parted.txt
lsblk -o NAME,SIZE,TYPE,FSTYPE,PARTLABEL /dev/vdb > output/lsblk.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj08-02
lab finish obj08-02
```

---

### obj08-03 — Criar XFS e montar temporariamente

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj08-03
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj08-03

sudo timeout --signal=TERM --kill-after=2s 30s mkfs.xfs -f -L RHCSA08XFS /dev/vdb1
sudo timeout --signal=TERM --kill-after=2s 30s mount /dev/vdb1 /mnt/rhcsa-xfs
echo OBJ08-XFS | sudo tee /mnt/rhcsa-xfs/obj08.txt
findmnt /mnt/rhcsa-xfs > output/findmnt.txt
lsblk -f /dev/vdb > output/lsblk.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj08-03
lab finish obj08-03
```

---

### obj08-04 — Montar XFS persistentemente por UUID

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj08-04
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj08-04

UUID=$(sudo blkid -s UUID -o value /dev/vdb1)
echo "UUID=$UUID /data1 xfs defaults 0 0" | sudo tee -a /etc/fstab
sudo systemctl daemon-reload
sudo timeout --signal=TERM --kill-after=2s 30s mount /data1
findmnt --verify > output/verify.txt
findmnt /data1 > output/findmnt.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj08-04
lab finish obj08-04
```

---

### obj08-05 — Criar swap persistente em partição

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj08-05
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj08-05

sudo timeout --signal=TERM --kill-after=2s 30s mkswap -L RHCSA08SWAP /dev/vde1
sudo swapon /dev/vde1
UUID=$(sudo blkid -s UUID -o value /dev/vde1)
echo "UUID=$UUID none swap defaults 0 0" | sudo tee -a /etc/fstab
sudo systemctl daemon-reload
swapon --show > output/swapon.txt
free -h > output/free.txt
findmnt --verify

exit
```

**No bastion, execute:**

```bash
lab grade obj08-05
lab finish obj08-05
```

---

### obj08-06 — Desafio integrado de Basic Storage

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj08-06
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj08-06

sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdb mklabel gpt
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdb mkpart basicdata xfs 1MiB 2049MiB
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdb mkpart basicswap linux-swap 2049MiB 3073MiB
sudo udevadm settle --timeout=15
sudo timeout --signal=TERM --kill-after=2s 30s mkfs.xfs -f -L BASIC08 /dev/vdb1
sudo timeout --signal=TERM --kill-after=2s 30s mkswap -L BASWAP08 /dev/vdb2
U1=$(sudo blkid -s UUID -o value /dev/vdb1)
U2=$(sudo blkid -s UUID -o value /dev/vdb2)
echo "UUID=$U1 /basicdata xfs defaults 0 0" | sudo tee -a /etc/fstab
echo "UUID=$U2 none swap defaults 0 0" | sudo tee -a /etc/fstab
sudo systemctl daemon-reload
sudo timeout --signal=TERM --kill-after=2s 30s mount /basicdata
sudo swapon /dev/vdb2
echo OBJ08-BASIC | sudo tee /basicdata/marker.txt
findmnt --verify
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdb unit MiB print > output/parted.txt
lsblk -f /dev/vdb > output/lsblk.txt
findmnt /basicdata > output/findmnt.txt
swapon --show > output/swapon.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj08-06
lab finish obj08-06
```

---

### obj08-07 — Criar PV, VG e LV

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj08-07
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj08-07

sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdc mklabel gpt
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdc mkpart lvm08 1MiB 4097MiB
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdc set 1 lvm on
sudo udevadm settle --timeout=15
sudo timeout --signal=TERM --kill-after=2s 30s pvcreate /dev/vdc1
sudo timeout --signal=TERM --kill-after=2s 30s vgcreate rhcsa_vgdata /dev/vdc1
sudo timeout --signal=TERM --kill-after=2s 30s lvcreate --yes --wipesignatures y -L 1536M -n rhcsa_lvdata rhcsa_vgdata
sudo pvs > output/pvs.txt
sudo vgs > output/vgs.txt
sudo lvs > output/lvs.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj08-07
lab finish obj08-07
```

---

### obj08-08 — Criar XFS em LV e persistir montagem

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj08-08
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj08-08

DEV=/dev/rhcsa_vgdata/rhcsa_lvdata
sudo timeout --signal=TERM --kill-after=2s 30s mkfs.xfs -f -L LVDATA08 "$DEV"
UUID=$(sudo blkid -s UUID -o value "$DEV")
echo "UUID=$UUID /lvdata xfs defaults 0 0" | sudo tee -a /etc/fstab
sudo systemctl daemon-reload
sudo timeout --signal=TERM --kill-after=2s 30s mount /lvdata
echo OBJ08-LVDATA | sudo tee /lvdata/marker.txt
findmnt --verify
findmnt /lvdata > output/findmnt.txt
lsblk -f > output/lsblk.txt
sudo lvs > output/lvs.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj08-08
lab finish obj08-08
```

---

### obj08-09 — Estender LV e filesystem XFS

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj08-09
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj08-09

sudo timeout --signal=TERM --kill-after=2s 30s lvextend -L 2G /dev/rhcsa_vgdata/rhcsa_lvdata
sudo timeout --signal=TERM --kill-after=2s 30s xfs_growfs /lvextend
sudo lvs > output/lvs.txt
df -h /lvextend > output/df.txt
sudo xfs_info /lvextend > output/xfs-info.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj08-09
lab finish obj08-09
```

---

### obj08-10 — Adicionar PV e estender VG

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj08-10
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj08-10

sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdd mklabel gpt
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdd mkpart pv2 1MiB 2049MiB
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdd set 1 lvm on
sudo udevadm settle --timeout=15
sudo timeout --signal=TERM --kill-after=2s 30s pvcreate /dev/vdd1
sudo timeout --signal=TERM --kill-after=2s 30s vgextend rhcsa_vgextend /dev/vdd1
sudo timeout --signal=TERM --kill-after=2s 30s lvcreate --yes --wipesignatures y -L 2G -n rhcsa_lvextra rhcsa_vgextend
sudo pvs > output/pvs.txt
sudo vgs > output/vgs.txt
sudo lvs > output/lvs.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj08-10
lab finish obj08-10
```

---

### obj08-11 — Criar swap em LVM

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj08-11
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj08-11

sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vde mklabel gpt
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vde mkpart pvswap 1MiB 1537MiB
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vde set 1 lvm on
sudo udevadm settle --timeout=15
sudo timeout --signal=TERM --kill-after=2s 30s pvcreate /dev/vde1
sudo timeout --signal=TERM --kill-after=2s 30s vgcreate rhcsa_vgswap /dev/vde1
sudo timeout --signal=TERM --kill-after=2s 30s lvcreate --yes --wipesignatures y -L 768M -n rhcsa_lvswap rhcsa_vgswap
sudo timeout --signal=TERM --kill-after=2s 30s mkswap -L LVSWAP08 /dev/rhcsa_vgswap/rhcsa_lvswap
sudo swapon /dev/rhcsa_vgswap/rhcsa_lvswap
UUID=$(sudo blkid -s UUID -o value /dev/rhcsa_vgswap/rhcsa_lvswap)
echo "UUID=$UUID none swap defaults 0 0" | sudo tee -a /etc/fstab
sudo systemctl daemon-reload
sudo pvs > output/pvs.txt
sudo vgs > output/vgs.txt
sudo lvs > output/lvs.txt
swapon --show > output/swapon.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj08-11
lab finish obj08-11
```

---

### obj08-12 — Desafio integrado de Storage e LVM

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj08-12
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj08-12

sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdc mklabel gpt
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdc mkpart pv1 1MiB 4097MiB
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdc set 1 lvm on
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdd mklabel gpt
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdd mkpart pv2 1MiB 2561MiB
sudo timeout --signal=TERM --kill-after=2s 30s parted -s /dev/vdd set 1 lvm on
sudo udevadm settle --timeout=15
sudo timeout --signal=TERM --kill-after=2s 30s pvcreate /dev/vdc1 /dev/vdd1
sudo timeout --signal=TERM --kill-after=2s 30s vgcreate rhcsa_vgfinal /dev/vdc1 /dev/vdd1
sudo timeout --signal=TERM --kill-after=2s 30s lvcreate --yes --wipesignatures y -L 2G -n rhcsa_data rhcsa_vgfinal
sudo timeout --signal=TERM --kill-after=2s 30s lvcreate --yes --wipesignatures y -L 512M -n rhcsa_swap rhcsa_vgfinal
sudo timeout --signal=TERM --kill-after=2s 30s mkfs.xfs -f -L FINAL08 /dev/rhcsa_vgfinal/rhcsa_data
DUUID=$(sudo blkid -s UUID -o value /dev/rhcsa_vgfinal/rhcsa_data)
echo "UUID=$DUUID /lvfinal xfs defaults 0 0" | sudo tee -a /etc/fstab
sudo systemctl daemon-reload
sudo timeout --signal=TERM --kill-after=2s 30s mount /lvfinal
echo OBJ08-FINAL | sudo tee /lvfinal/marker.txt
sudo timeout --signal=TERM --kill-after=2s 30s mkswap -L FINALSWAP08 /dev/rhcsa_vgfinal/rhcsa_swap
SUUID=$(sudo blkid -s UUID -o value /dev/rhcsa_vgfinal/rhcsa_swap)
echo "UUID=$SUUID none swap defaults 0 0" | sudo tee -a /etc/fstab
sudo swapon /dev/rhcsa_vgfinal/rhcsa_swap
sudo timeout --signal=TERM --kill-after=2s 30s lvextend -L 3G /dev/rhcsa_vgfinal/rhcsa_data
sudo timeout --signal=TERM --kill-after=2s 30s xfs_growfs /lvfinal
findmnt --verify
sudo pvs > output/pvs.txt
sudo vgs > output/vgs.txt
sudo lvs > output/lvs.txt
findmnt /lvfinal > output/findmnt.txt
swapon --show > output/swapon.txt
df -h /lvfinal > output/df.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj08-12
lab finish obj08-12
```

---

## Referências de consulta

- [Enunciados — Objective 08](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab/tree/main/labs/08-storage)
- [Scripts de referência — obj08-01 a obj08-12](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab/tree/main/tests/reference-solutions)

**Validação:** os comandos foram confrontados com os enunciados e scripts de referência da branch `main` em 12/10/2026. A sintaxe Bash de todos os blocos foi verificada. A execução de `lab start/grade/finish` nas VMs não foi realizada nesta sessão.
