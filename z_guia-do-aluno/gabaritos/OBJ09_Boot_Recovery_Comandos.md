# RHCSA EX200 v10 — Gabarito Operacional

## Objective 09 — Boot, GRUB & Recovery

**Referência:** repositório [`eduardoandradej/rhcsa-ex200-v10-lab`](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab), branch `main` — `prompt.pt.md`, `tests/reference-solutions/obj09-*.sh`, `solution.md` dos drills manuais e respectivos graders.  
**Plataforma local:** RHEL 9.8 • **Referência de estudo:** RHEL 10.  
**Execução:** os cinco exercícios `ready` utilizam `lab start`, `lab grade` e `lab finish` no `bastion`, com comandos no `servera`. Os itens `obj09-04` e `obj09-06` são **manual-only**, exigem console do host KVM e **não usam `lab start`, `lab grade` ou `lab finish`**.  
**Sequência:** um exercício por vez. Faça os exercícios manuais somente em uma VM de laboratório, preferencialmente com snapshot de recuperação disponível. **Não altere nem remova os argumentos `console=` do kernel** durante a recuperação por GRUB.

---

### obj09-01 — Inventário de boot, kernel e GRUB

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj09-01
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj09-01

uname -r > output/kernel.txt
cat /proc/cmdline > output/cmdline.txt
sudo grubby --default-kernel > output/default-kernel.txt
sudo grubby --info=ALL > output/grubby.txt
systemctl get-default > output/default-target.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj09-01
lab finish obj09-01
```

---

### obj09-02 — Argumentos persistentes do kernel

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj09-02
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj09-02

sudo grubby --info=ALL
sudo grubby --update-kernel=ALL --args="systemd.show_status=1"
sudo grubby --info=ALL > output/grubby.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj09-02
lab finish obj09-02
```

---

### obj09-03 — Gerenciar o target padrão do systemd

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj09-03
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj09-03

systemctl get-default
sudo systemctl set-default multi-user.target
systemctl get-default > output/default-target.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj09-03
lab finish obj09-03
```

---

### obj09-04 — Rescue e emergency pelo console (manual-only)

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab status
lab show obj09-04
```

**No host KVM, execute (terminal com ambiente gráfico):**

```bash
sudo virsh -c qemu:///system list --all
virt-manager --connect qemu:///system
```

**No virt-manager, execute manualmente:**

1. Abra o console gráfico da VM **servera**.
2. Reinicie a VM pelo próprio console ou execute em outro terminal do **host KVM**:

```bash
sudo virsh -c qemu:///system reboot servera
```

3. No menu GRUB, selecione a entrada de inicialização e pressione **`e`**.
4. Na linha iniciada por `linux` ou `linuxefi`, acrescente **ao final**:

```text
systemd.unit=emergency.target
```

5. Inicialize a entrada editada com **Ctrl+X**.
6. No shell de manutenção do **servera**, após a autenticação solicitada, execute:

```bash
findmnt -no SOURCE,FSTYPE,OPTIONS /
mount -o remount,rw /
findmnt -no SOURCE,FSTYPE,OPTIONS /
sync
reboot
```

**No bastion, após retornar ao boot normal, execute:**

```bash
ssh student@servera 'systemctl get-default'
ssh student@servera 'systemctl is-system-running || true'
```

**Não execute `lab start`, `lab grade` ou `lab finish` para `obj09-04`.** O parâmetro do GRUB deve ser **temporário**, válido somente para o boot editado.

---

### obj09-05 — Diagnosticar e corrigir falha de fstab

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj09-05
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj09-05

sudo mount -a || true
UUID=$(sudo blkid -s UUID -o value /dev/vdb1)
sudo mkdir -p /srv/recovery09
sudo sed -i '\|[[:space:]]/srv/recovery09[[:space:]]|d' /etc/fstab
echo "UUID=$UUID /srv/recovery09 xfs defaults 0 0" | sudo tee -a /etc/fstab >/dev/null
sudo systemctl daemon-reload
sudo mount -a
sudo findmnt --verify > output/verify.txt
findmnt /srv/recovery09 > output/findmnt.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj09-05
lab finish obj09-05
```

---

### obj09-06 — Recuperação de acesso root pelo boot loader (manual-only)

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab status
lab show obj09-06
```

**No host KVM, execute (terminal com ambiente gráfico):**

```bash
sudo virsh -c qemu:///system list --all
virt-manager --connect qemu:///system
```

**No virt-manager, execute manualmente — alternativa sem mídia em VM de treinamento:**

1. Abra o console gráfico de **servera**.
2. Reinicie a VM pelo console ou execute em outro terminal do **host KVM**:

```bash
sudo virsh -c qemu:///system reboot servera
```

3. No GRUB, selecione a entrada e pressione **`e`**.
4. Na linha do kernel (`linux` ou `linuxefi`), substitua o parâmetro `ro` por `rw` **e acrescente** o parâmetro abaixo, **sem remover `console=`**:

```text
init=/bin/bash
```

5. Inicialize a entrada editada com **Ctrl+X**.
6. No shell de recuperação do **servera**, execute:

```bash
mount -o remount,rw /
passwd root
touch /.autorelabel
sync
reboot -f
```

**No servera, após o boot normal e o relabeling SELinux, execute:**

```bash
getenforce
su -
```

**No shell root, execute:**

```bash
id -un
exit
```

**No bastion, para validar o retorno ao acesso SSH, execute:**

```bash
ssh student@servera 'hostname -f; getenforce'
```

**Não execute `lab start`, `lab grade` ou `lab finish` para `obj09-06`.** A senha root será solicitada interativamente por `passwd root` e, posteriormente, por `su -`. O primeiro boot pode demorar por causa do relabeling SELinux. Para a referência RHEL 10, prefira repetir a recuperação com mídia de rescue no ambiente RHLS Premium, como orienta o enunciado do projeto.

---

### obj09-07 — Desafio integrado de boot e recuperação

**No bastion, execute:**

```bash
cd ~/rhcsa-ex200-v10-lab
lab start obj09-07
ssh student@servera
```

**No servera, execute:**

```bash
cd /home/student/rhcsa-lab/obj09-07

sudo systemctl set-default multi-user.target
sudo grubby --update-kernel=ALL --args="systemd.show_status=1"
sudo grubby --info=ALL > output/grubby.txt
systemctl get-default > output/default-target.txt
cat /proc/cmdline > output/current-cmdline.txt
sudo findmnt --verify > output/fstab-verify.txt

exit
```

**No bastion, execute:**

```bash
lab grade obj09-07
lab finish obj09-07
```

---

## Referências de consulta

- [Enunciados — Objective 09](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab/tree/main/labs/09-boot-recovery)
- [Soluções de referência — exercícios automatizados](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab/tree/main/tests/reference-solutions)
- [Drill `obj09-04` — `solution.md`](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab/blob/main/labs/09-boot-recovery/04-rescue-emergency-console/solution.md)
- [Drill `obj09-06` — `solution.md`](https://github.com/eduardoandradej/rhcsa-ex200-v10-lab/blob/main/labs/09-boot-recovery/06-root-access-recovery/solution.md)

**Validação:** comandos dos cinco laboratórios automatizados conferidos com os scripts `tests/reference-solutions/obj09-*.sh`; os dois manuais foram alinhados aos enunciados e às notas de recuperação. Sintaxe Bash dos blocos verificada. **Não houve execução real nas VMs nem confirmação de notas do grader nesta sessão.** A sequência gráfica do GRUB e os comandos de reinicialização são instruções operacionais complementares ao material do repositório.
