# 07 — Baseline e snapshots

[Índice](README.md) · [Home](../../README.md) · [Anterior](06-validacao-ansible.md) · [Próximo](08-primeiro-lab.md)

**Onde executar:** primeiro no `bastion`, depois no **host KVM/libvirt**.

Esta etapa cria um ponto de recuperação consistente antes do início dos exercícios.

O laboratório foi projetado com uma separação clara de responsabilidades:

```text
bastion
└── plano de controle estável
    ├── Git
    ├── Ansible
    ├── CLI lab
    └── estado de execução dos exercícios

servera / serverb
└── nós descartáveis de prática
    ├── alterações dos exercícios
    ├── serviços
    ├── armazenamento
    ├── rede
    └── cenários de troubleshooting
```

Por isso, o baseline recomendado desta versão é:

- manter o `bastion` estável e versionado pelo Git;
- criar snapshots de `servera` e `serverb`;
- utilizar `lab finish` como mecanismo normal de limpeza;
- utilizar snapshots como mecanismo de recuperação quando a limpeza normal não for suficiente.

> Snapshot não substitui backup. Ele é um checkpoint local do laboratório.

---

## 7.1 Entender a diferença entre `lab finish` e snapshot

O comando:

```bash
lab finish
```

é o mecanismo normal de encerramento de um exercício.

Ele executa o arquivo:

```text
finish.yml
```

do laboratório ativo.

Quando a limpeza termina com sucesso, o CLI remove o estado ativo do exercício e apresenta:

```text
LAB FINISHED
```

Se o playbook de limpeza falhar, o estado ativo **não é apagado**.

Isso é intencional: uma falha de cleanup não deve ser escondida.

Um snapshot tem outra função.

Ele permite retornar uma VM a um ponto anterior quando, por exemplo:

- um exercício alterou profundamente o sistema;
- a VM não inicializa corretamente;
- houve erro manual fora do escopo do exercício;
- a limpeza normal não consegue restaurar o nó;
- um exercício de armazenamento deixou o disco em estado inesperado;
- um cenário de recuperação precisa ser repetido do zero.

Fluxo normal:

```text
lab start
    ↓
resolver exercício
    ↓
lab grade
    ↓
lab finish
    ↓
próximo exercício
```

Fluxo de contingência:

```text
lab finish falhou
        ↓
diagnosticar
        ↓
restaurar snapshot, se necessário
        ↓
revalidar ambiente
        ↓
sincronizar estado do CLI
```

---

## 7.2 Não criar o baseline com laboratório ativo

No `bastion`:

```bash
cd ~/rhcsa-ex200-v10-lab
```

Execute:

```bash
lab status
```

A seção:

```text
Lab State
```

deve mostrar:

```text
Active      none
```

Se existir um exercício ativo, finalize-o:

```bash
lab finish
```

ou, explicitamente:

```bash
lab finish ID_DO_EXERCICIO
```

Depois:

```bash
lab status
```

Não crie snapshots de baseline enquanto o CLI indicar um exercício ativo.

---

## 7.3 Validar o ambiente antes do snapshot

Ainda no `bastion`, confirme o plano de controle:

```bash
lab status
```

O ambiente deve apresentar:

```text
bastion   ONLINE
servera   ONLINE
serverb   ONLINE
```

e:

```text
Environment: READY
```

Entre no diretório Ansible:

```bash
cd ~/rhcsa-ex200-v10-lab/ansible
```

Teste:

```bash
ansible all -m ansible.builtin.ping
```

Valide o baseline de sistema operacional:

```bash
ansible-playbook playbooks/validate.yml
```

Valide as dependências:

```bash
ansible-playbook playbooks/00-validate-dependencies.yml
```

Somente crie o snapshot depois que essas validações estiverem corretas.

---

## 7.4 Registrar a versão do projeto utilizada no baseline

Antes de criar o checkpoint, registre a versão atual do repositório.

No `bastion`:

```bash
cd ~/rhcsa-ex200-v10-lab
```

Execute:

```bash
git status
```

Depois:

```bash
git log -1 --oneline --decorate
```

E:

```bash
git describe --tags --always
```

Uma árvore limpa é o estado preferido:

```text
nothing to commit, working tree clean
```

Anote o commit ou tag utilizado.

Isso permite relacionar:

```text
versão do código
+
versão da documentação
+
baseline das VMs
```

---

## 7.5 Por que o bastion não é o alvo principal do snapshot

Os exercícios automatizados desta versão atuam em:

```text
servera
serverb
```

O `bastion` funciona como plano de controle.

Ele contém:

```text
repositório Git
CLI lab
estado ativo em .state/
chaves SSH
Ansible
```

Reverter o `bastion` para um snapshot antigo pode também reverter:

- commits;
- atualizações do repositório;
- documentação;
- arquivos de estado do CLI;
- `known_hosts`;
- configurações SSH.

Por isso, a política recomendada é:

```text
bastion  → estável, preservado e atualizado por Git
servera  → descartável, protegido por snapshot
serverb  → descartável, protegido por snapshot
```

Um snapshot do `bastion` pode ser criado como proteção adicional, mas não é necessário para o fluxo normal deste projeto.

---

## 7.6 Ir para o host KVM

A partir deste ponto, os comandos devem ser executados no **host KVM/libvirt**.

Não exponha acesso administrativo ao libvirt para o `bastion` apenas para automatizar esta etapa.

Confirme o host:

```bash
hostnamectl
```

Confira as VMs:

```bash
sudo virsh -c qemu:///system list --all
```

Devem existir:

```text
bastion
servera
serverb
```

---

## 7.7 Inspecionar a topologia de discos antes do snapshot

Confira `servera`:

```bash
sudo virsh -c qemu:///system domblklist servera
```

Confira `serverb`:

```bash
sudo virsh -c qemu:///system domblklist serverb
```

A topologia esperada é:

```text
servera
vda  30 GiB
vdb   5 GiB
vdc   5 GiB
vdd   3 GiB
vde   2 GiB
```

e:

```text
serverb
vda  30 GiB
vdb   5 GiB
vdc   3 GiB
```

Todos os discos graváveis utilizados por este procedimento devem ser QCOW2.

---

## 7.8 Confirmar o formato dos discos

Obtenha os caminhos dos discos:

```bash
sudo virsh -c qemu:///system domblklist servera --details
```

```bash
sudo virsh -c qemu:///system domblklist serverb --details
```

Para cada arquivo de disco, consulte:

```bash
sudo qemu-img info /CAMINHO/DO/DISCO.qcow2
```

Confirme:

```text
file format: qcow2
```

Não aplique este procedimento sem adaptação se sua VM utilizar:

- discos RAW;
- LVM block devices;
- passthrough de disco;
- volumes de storage externos;
- backing chains que você não compreende;
- storage compartilhado.

O exemplo desta documentação assume discos QCOW2 locais.

---

## 7.9 Verificar snapshots existentes

Antes de criar novos snapshots:

```bash
sudo virsh -c qemu:///system snapshot-list servera
```

```bash
sudo virsh -c qemu:///system snapshot-list serverb
```

O nome adotado por este guia é:

```text
baseline-pre-labs
```

Não crie outro snapshot com o mesmo nome se ele já existir.

Se houver um baseline anterior, primeiro decida se ele ainda precisa ser preservado.

---

## 7.10 Desligar os nós gerenciados de forma limpa

O snapshot de baseline será criado com os nós desligados.

Isso reduz a quantidade de estado transitório gravado no checkpoint e simplifica a recuperação.

No host KVM:

```bash
sudo virsh -c qemu:///system shutdown servera
```

```bash
sudo virsh -c qemu:///system shutdown serverb
```

Aguarde:

```bash
sudo virsh -c qemu:///system list --all
```

O estado esperado é:

```text
servera   shut off
serverb   shut off
```

Não utilize:

```bash
virsh destroy
```

como procedimento normal de desligamento.

`destroy` equivale a interromper abruptamente a alimentação da VM e deve ser reservado para situações em que o desligamento normal não é possível.

---

## 7.11 Confirmar que os nós realmente desligaram

Uma verificação objetiva:

```bash
sudo virsh -c qemu:///system domstate servera
```

Esperado:

```text
shut off
```

Depois:

```bash
sudo virsh -c qemu:///system domstate serverb
```

Esperado:

```text
shut off
```

Não prossiga se alguma VM ainda estiver em execução.

---

## 7.12 Criar o snapshot de servera

Execute:

```bash
sudo virsh -c qemu:///system snapshot-create-as \
  servera \
  baseline-pre-labs \
  --description "Baseline RHCSA limpo antes dos laboratórios"
```

Depois valide:

```bash
sudo virsh -c qemu:///system snapshot-info \
  servera \
  baseline-pre-labs
```

Consulte também:

```bash
sudo virsh -c qemu:///system snapshot-list servera
```

O snapshot:

```text
baseline-pre-labs
```

deve aparecer na lista.

---

## 7.13 Criar o snapshot de serverb

Execute:

```bash
sudo virsh -c qemu:///system snapshot-create-as \
  serverb \
  baseline-pre-labs \
  --description "Baseline RHCSA limpo antes dos laboratórios"
```

Valide:

```bash
sudo virsh -c qemu:///system snapshot-info \
  serverb \
  baseline-pre-labs
```

E:

```bash
sudo virsh -c qemu:///system snapshot-list serverb
```

---

## 7.14 Inspecionar o XML dos snapshots

Confira `servera`:

```bash
sudo virsh -c qemu:///system snapshot-dumpxml \
  servera \
  baseline-pre-labs
```

Depois `serverb`:

```bash
sudo virsh -c qemu:///system snapshot-dumpxml \
  serverb \
  baseline-pre-labs
```

Essa inspeção é importante porque a VM possui múltiplos discos.

Não considere o baseline validado apenas porque o nome do snapshot apareceu na lista.

Confirme que o snapshot representa a topologia esperada da VM.

---

## 7.15 Opcional: snapshot do bastion

O snapshot do `bastion` é opcional.

Use-o somente se desejar um checkpoint completo da estação de controle e entender que uma restauração posterior poderá reverter o repositório Git e os arquivos locais.

Primeiro confirme:

```bash
cd ~/rhcsa-ex200-v10-lab
git status
```

no `bastion`.

Depois, no host KVM, desligue:

```bash
sudo virsh -c qemu:///system shutdown bastion
```

Aguarde:

```bash
sudo virsh -c qemu:///system domstate bastion
```

Quando estiver:

```text
shut off
```

crie:

```bash
sudo virsh -c qemu:///system snapshot-create-as \
  bastion \
  baseline-pre-labs \
  --description "Baseline opcional do plano de controle"
```

Valide:

```bash
sudo virsh -c qemu:///system snapshot-info \
  bastion \
  baseline-pre-labs
```

Se você optar por **não** criar o snapshot do `bastion`, mantenha-o protegido por:

- Git;
- backups independentes quando necessário;
- disciplina para não realizar exercícios diretamente nele.

---

## 7.16 Reiniciar as VMs

Inicie `servera`:

```bash
sudo virsh -c qemu:///system start servera
```

Inicie `serverb`:

```bash
sudo virsh -c qemu:///system start serverb
```

Se o `bastion` também foi desligado:

```bash
sudo virsh -c qemu:///system start bastion
```

Confira:

```bash
sudo virsh -c qemu:///system list
```

---

## 7.17 Aguardar o sistema operacional ficar disponível

O estado `running` do libvirt não significa que o SSH já está pronto.

Aguarde alguns segundos.

No `bastion`, teste:

```bash
ssh -o BatchMode=yes \
  -o ConnectTimeout=5 \
  servera \
  hostname -f
```

Depois:

```bash
ssh -o BatchMode=yes \
  -o ConnectTimeout=5 \
  serverb \
  hostname -f
```

Resultados esperados:

```text
servera.lab.test
```

e:

```text
serverb.lab.test
```

---

## 7.18 Revalidar o ambiente depois do snapshot

No `bastion`:

```bash
cd ~/rhcsa-ex200-v10-lab
```

Execute:

```bash
lab status
```

O ambiente deve voltar a:

```text
Environment: READY
```

Confirme que não existe exercício ativo:

```text
Active      none
```

Entre no diretório Ansible:

```bash
cd ~/rhcsa-ex200-v10-lab/ansible
```

Teste:

```bash
ansible all -m ansible.builtin.ping
```

Todos os hosts devem responder com sucesso.

---

# Restauração

## 7.19 Quando utilizar o snapshot

O snapshot não deve substituir `lab finish` no uso diário.

Primeiro tente:

```bash
lab finish
```

Considere restaurar o snapshot quando:

- a VM não inicializa;
- o exercício alterou o armazenamento além da capacidade do cleanup;
- houve uma modificação manual fora do cenário;
- a limpeza falha repetidamente;
- você deseja voltar ao estado inicial do laboratório para uma nova sequência de estudos.

Para exercícios que envolvem simultaneamente `servera` e `serverb`, considere restaurar os dois nós para preservar a consistência do cenário.

---

## 7.20 Preservar dados antes de restaurar

Uma restauração descarta alterações posteriores ao snapshot na VM restaurada.

Antes de reverter, verifique se existe algo que precisa ser preservado.

Em especial:

```text
arquivos pessoais
anotações
scripts
configurações criadas manualmente
evidências de troubleshooting
```

O laboratório é descartável, mas isso não significa que dados pessoais devam ser descartados sem intenção.

---

## 7.21 Desligar antes da restauração

No host KVM:

```bash
sudo virsh -c qemu:///system shutdown servera
sudo virsh -c qemu:///system shutdown serverb
```

Aguarde:

```bash
sudo virsh -c qemu:///system list --all
```

Se apenas uma VM será restaurada, desligue apenas essa VM.

Não execute uma restauração de snapshot sem confirmar o estado da máquina.

---

## 7.22 Restaurar servera

Confira primeiro:

```bash
sudo virsh -c qemu:///system snapshot-list servera
```

Restaure:

```bash
sudo virsh -c qemu:///system snapshot-revert \
  servera \
  baseline-pre-labs
```

Confira:

```bash
sudo virsh -c qemu:///system domstate servera
```

Se permanecer desligada, inicie:

```bash
sudo virsh -c qemu:///system start servera
```

---

## 7.23 Restaurar serverb

Confira:

```bash
sudo virsh -c qemu:///system snapshot-list serverb
```

Restaure:

```bash
sudo virsh -c qemu:///system snapshot-revert \
  serverb \
  baseline-pre-labs
```

Depois:

```bash
sudo virsh -c qemu:///system domstate serverb
```

Se necessário:

```bash
sudo virsh -c qemu:///system start serverb
```

---

## 7.24 Restaurar os dois nós

Quando o cenário envolveu ambos:

```bash
sudo virsh -c qemu:///system snapshot-revert \
  servera \
  baseline-pre-labs
```

```bash
sudo virsh -c qemu:///system snapshot-revert \
  serverb \
  baseline-pre-labs
```

Depois:

```bash
sudo virsh -c qemu:///system start servera
sudo virsh -c qemu:///system start serverb
```

---

## 7.25 Revalidar SSH após restauração

No `bastion`:

```bash
ssh -o BatchMode=yes servera hostname -f
```

```bash
ssh -o BatchMode=yes serverb hostname -f
```

Se aparecer aviso de host key alterada, não remova a entrada automaticamente.

Confirme a fingerprint diretamente pelo console da VM.

Um snapshot criado corretamente deve restaurar também a identidade SSH existente no momento em que o baseline foi criado.

---

## 7.26 Revalidar o Ansible após restauração

No `bastion`:

```bash
cd ~/rhcsa-ex200-v10-lab/ansible
```

Execute:

```bash
ansible all -m ansible.builtin.ping
```

Depois:

```bash
ansible all \
  -m ansible.builtin.command \
  -a 'hostname -f'
```

Resultados esperados:

```text
bastion.lab.test
servera.lab.test
serverb.lab.test
```

---

## 7.27 Sincronizar o estado do CLI depois de uma recuperação manual

O estado de exercício ativo é armazenado no `bastion`, em:

```text
.state/active.json
```

Esse diretório é runtime e está ignorado pelo Git.

No uso normal, **não manipule esse arquivo manualmente**.

Primeiro consulte:

```bash
lab status
```

### Se não houver laboratório ativo

Nenhuma ação adicional é necessária.

### Se ainda houver um laboratório ativo após restaurar as VMs

Isso pode acontecer quando um `lab finish` falhou e as VMs foram recuperadas manualmente por snapshot.

Primeiro tente novamente:

```bash
lab finish
```

Se o cleanup agora terminar com sucesso, o próprio CLI limpará o estado.

Somente em uma recuperação excepcional, quando:

- as VMs já foram comprovadamente restauradas ao baseline;
- não existe mais cenário ativo nos nós;
- `lab finish` não consegue concluir por um problema externo ao estado das VMs;

pode ser necessário remover manualmente o estado runtime:

```bash
rm -f ~/rhcsa-ex200-v10-lab/.state/active.json
```

Depois:

```bash
lab status
```

Esse procedimento é uma recuperação administrativa, não o fluxo normal do laboratório.

---

## 7.28 Revalidar o baseline completo após restauração

Para uma recuperação importante, execute novamente:

```bash
cd ~/rhcsa-ex200-v10-lab/ansible
```

```bash
ansible-playbook playbooks/validate.yml
```

Depois:

```bash
ansible-playbook \
  playbooks/00-validate-dependencies.yml
```

Volte:

```bash
cd ~/rhcsa-ex200-v10-lab
```

Confira:

```bash
lab status
```

Só retome os exercícios quando o ambiente estiver novamente consistente.

---

# Manutenção dos snapshots

## 7.29 Não confundir snapshot com backup

Snapshots internos ficam associados aos discos e ao armazenamento do host.

Eles não protegem contra:

- perda do SSD do hospedeiro;
- corrupção do arquivo QCOW2;
- exclusão acidental da VM;
- perda do diretório `/var/lib/libvirt`;
- falha completa do host.

Para proteger o ambiente contra esses eventos, utilize backup independente.

---

## 7.30 Antes de copiar um QCOW2

Não copie simplesmente um arquivo de disco que está sendo gravado por uma VM em execução.

Para produzir uma cópia consistente:

1. desligue a VM; ou
2. utilize um procedimento de backup compatível com libvirt/QEMU.

Para este projeto local, o caminho mais simples é desligar a VM antes da cópia.

---

## 7.31 Inspecionar snapshots periodicamente

No host KVM:

```bash
sudo virsh -c qemu:///system snapshot-list servera
```

```bash
sudo virsh -c qemu:///system snapshot-list serverb
```

Snapshots acumulados aumentam a complexidade de manutenção e podem aumentar o consumo de armazenamento.

Mantenha apenas checkpoints que tenham uma finalidade conhecida.

---

## 7.32 Verificar espaço em disco

No host:

```bash
df -h /var/lib/libvirt
```

Confira também o tamanho dos arquivos:

```bash
sudo du -sh /var/lib/libvirt/images/*
```

E informações do QCOW2:

```bash
sudo qemu-img info \
  /var/lib/libvirt/images/servera.qcow2
```

```bash
sudo qemu-img info \
  /var/lib/libvirt/images/serverb.qcow2
```

Não espere o filesystem do host ficar sem espaço antes de limpar snapshots antigos ou aumentar a capacidade.

---

## 7.33 Remover um snapshot antigo

Antes de remover qualquer snapshot, confirme:

```bash
sudo virsh -c qemu:///system snapshot-list servera
```

Depois, se você tiver certeza de que o snapshot não será mais necessário:

```bash
sudo virsh -c qemu:///system snapshot-delete \
  servera \
  NOME_DO_SNAPSHOT
```

Para `serverb`:

```bash
sudo virsh -c qemu:///system snapshot-delete \
  serverb \
  NOME_DO_SNAPSHOT
```

Nunca remova snapshots apenas para “limpar a lista” sem compreender sua função.

---

## 7.34 Atualizar o baseline após uma nova versão do projeto

Uma atualização do Git não atualiza automaticamente os snapshots.

Quando uma nova versão do projeto exigir mudanças no baseline:

1. atualize o repositório;
2. aplique as mudanças de infraestrutura documentadas;
3. execute novamente as validações da etapa 06;
4. confirme que nenhum laboratório está ativo;
5. crie um novo snapshot com nome diferente.

Exemplo:

```text
baseline-v1.8.4
baseline-v1.9.0
```

Isso permite distinguir claramente a versão do ambiente.

Não substitua silenciosamente um baseline antigo sem registrar a mudança.

---

## 7.35 Estratégia de nomes recomendada

Para um ambiente pessoal simples:

```text
baseline-pre-labs
```

é suficiente.

Para ambientes mantidos por mais tempo:

```text
baseline-v1.8.4
baseline-v1.9.0
```

é mais informativo.

O nome do snapshot deve permitir responder:

```text
“Que versão do ambiente estou restaurando?”
```

---

## 7.36 Problemas comuns

### `snapshot-create-as` informa que o snapshot já existe

Confira:

```bash
sudo virsh -c qemu:///system snapshot-list servera
```

Não reutilize o mesmo nome sem decidir o que fazer com o snapshot existente.

Crie um novo nome ou remova conscientemente o antigo.

---

### O snapshot falha porque um disco não suporta a operação

Confira:

```bash
sudo virsh -c qemu:///system domblklist servera --details
```

Depois:

```bash
sudo qemu-img info /CAMINHO/DO/DISCO
```

Este roteiro pressupõe discos QCOW2 locais.

Não converta ou remova discos apenas para forçar o snapshot sem compreender o impacto.

---

### A VM não desliga com `virsh shutdown`

Confira:

```bash
sudo virsh -c qemu:///system domstate servera
```

Aguarde o sistema operacional responder ao evento ACPI.

Se necessário, entre pelo console e execute:

```bash
sudo systemctl poweroff
```

Use `virsh destroy` apenas como último recurso.

---

### A VM foi restaurada, mas o Ansible continua falhando

Teste:

```bash
ssh -o BatchMode=yes servera hostname -f
```

Depois:

```bash
cd ~/rhcsa-ex200-v10-lab/ansible
ansible servera -m ansible.builtin.ping
```

Confira:

- hostname;
- endereço IP;
- SSH host key;
- usuário `student`;
- `sudo -n`;
- Python.

---

### `lab status` mostra exercício ativo depois do snapshot revert

O snapshot de `servera` ou `serverb` não modifica o estado armazenado no `bastion`.

Primeiro tente:

```bash
lab finish
```

Somente depois de confirmar que os nós já estão no baseline considere a recuperação manual do estado runtime descrita nesta página.

---

### O repositório do bastion voltou para uma versão antiga

Isso pode ocorrer se você optou por criar e restaurar um snapshot do `bastion`.

Confira:

```bash
cd ~/rhcsa-ex200-v10-lab
git status
git log -1 --oneline --decorate
```

Atualize o Git conscientemente antes de continuar.

Esse é um dos motivos pelos quais o snapshot do `bastion` é opcional.

---

## 7.37 Critério para concluir a etapa

Antes de iniciar o primeiro exercício, confirme:

```text
[ ] nenhum laboratório está ativo

[ ] lab status mostra Environment: READY
[ ] ansible all -m ping funciona
[ ] validate.yml passa
[ ] validação de dependências passa

[ ] versão do Git utilizada no baseline foi identificada

[ ] servera utiliza discos QCOW2 compatíveis com o plano de snapshot
[ ] serverb utiliza discos QCOW2 compatíveis com o plano de snapshot

[ ] servera possui snapshot de baseline
[ ] serverb possui snapshot de baseline

[ ] snapshots foram inspecionados e validados

[ ] servera voltou a iniciar normalmente
[ ] serverb voltou a iniciar normalmente

[ ] SSH continua funcional
[ ] Ansible continua funcional

[ ] bastion permanece estável e em estado conhecido
```

O ambiente está agora protegido por dois níveis complementares:

```text
lab finish
└── limpeza normal de cada exercício

snapshot
└── recuperação do nó quando a limpeza normal não é suficiente
```

Continue para:

[08 — Primeiro exercício](08-primeiro-lab.md)

[Índice](README.md) · [Home](../../README.md) · [Anterior](06-validacao-ansible.md) · [Próximo](08-primeiro-lab.md)
