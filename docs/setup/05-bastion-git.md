# 05 — Preparação do bastion e clonagem

[Índice](README.md) · [Home](../../README.md) · [Anterior](04-configuracao-vms.md) · [Próximo](06-validacao-ansible.md)

**Onde executar:** bastion, conectado como `student`. O projeto deve ficar em `/home/student/rhcsa-ex200-v10-lab`, conforme o inventário atual.

## Instalar dependências antes de clonar

```bash
sudo dnf install -y git ansible-core python3 python3-pyyaml openssh-clients
python3 -c 'import yaml; print("PyYAML OK")'
git --version
ansible --version
python3 --version
```

Se algum pacote não estiver disponível, resolva a origem dos pacotes antes de avançar.

## Clonar o repositório

```bash
cd ~
git clone https://github.com/eduardoandradej/rhcsa-ex200-v10-lab.git
cd ~/rhcsa-ex200-v10-lab
git remote -v
```

Se já tiver o projeto, não clone por cima. Confira `git status` e sincronize sua cópia após preservar alterações locais. O clone público permite leitura sem autenticação; envio de commits exige uma credencial autorizada.

## SSH dedicado

Crie a chave somente se ela ainda não existir:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
if [ ! -f ~/.ssh/id_ed25519_rhcsa_lab ]; then
  ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_rhcsa_lab -C rhcsa-lab
fi
```

Se usar passphrase, carregue a chave no `ssh-agent` da sessão antes de executar o Ansible. Copie apenas a chave pública:

```bash
ssh-copy-id -i ~/.ssh/id_ed25519_rhcsa_lab.pub student@servera
ssh-copy-id -i ~/.ssh/id_ed25519_rhcsa_lab.pub student@serverb
ssh -i ~/.ssh/id_ed25519_rhcsa_lab student@servera hostname -f
ssh -i ~/.ssh/id_ed25519_rhcsa_lab student@serverb hostname -f
```

Na primeira conexão, confira a fingerprint do host pelo console (`ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub`) antes de aceitar. Se uma VM for reinstalada ou um snapshot recuperar chaves diferentes, investigue a mudança e atualize somente a entrada correspondente em `known_hosts`.

Para que `ssh servera` e `ssh serverb` usem a mesma chave da automação, adicione a `~/.ssh/config`, sem duplicar blocos existentes:

```sshconfig
Host servera
    HostName 192.168.100.11
    User student
    IdentityFile ~/.ssh/id_ed25519_rhcsa_lab
    IdentitiesOnly yes

Host serverb
    HostName 192.168.100.12
    User student
    IdentityFile ~/.ssh/id_ed25519_rhcsa_lab
    IdentitiesOnly yes
```

```bash
chmod 600 ~/.ssh/config
ssh -o BatchMode=yes servera hostname -f
ssh -o BatchMode=yes serverb hostname -f
```

## Instalar o comando lab

```bash
cd ~/rhcsa-ex200-v10-lab
bash bootstrap/10-install-lab-cli.sh
source ~/.bashrc
lab --version
lab list
```

O instalador usa o wrapper do projeto e cria um link em `~/.local/bin`. O código atual também requer PyYAML. Nunca copie a chave privada para o Git.

**Antes de avançar:** CLI instalado e conexões SSH não interativas funcionando.

[Índice](README.md) · [Home](../../README.md) · [Anterior](04-configuracao-vms.md) · [Próximo](06-validacao-ansible.md)
