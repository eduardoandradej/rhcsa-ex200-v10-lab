# Importação do pacote de documentação KVM

Este é um pacote incremental para `eduardoandradej/rhcsa-ex200-v10-lab`.
Ele substitui a home (`README.md`) e o índice de instalação (`docs/setup/README.md`), adiciona oito guias e esta instrução. O código de `labctl`, os exercícios, inventário e scripts de bootstrap permanecem os da sua cópia do projeto.

A documentação foi preparada a partir do repositório público no commit `b9e846a` e da estrutura das entregas disponíveis até 2E. Ela documenta as etapas que faltavam na home; não transforma funcionalidades pendentes (reset integrado e novos cenários) em funcionalidades concluídas.

## Revisão v3

Adiciona links oficiais de imagens/checksums, caminho principal Ubuntu e alternativa Rocky Linux 9.8. Corrige a referência de hospedeiro do pacote anterior. Registra a coleta real do hospedeiro: ThinkPad T430, Ubuntu 24.04.5 LTS, i5-3320M (2 núcleos/4 threads), 15 GiB de RAM reportados, swap 4 GiB e SSD Kingston de 240 GB. Mantém o dimensionamento sugerido das VMs separado dos recursos físicos confirmados. A alternativa Rocky para as VMs exige adaptação e não é declarada validada.

## Aplicar no bastion

Transfira o arquivo `rhcsa-ex200-v10-lab-docs-kvm-v3.tar.gz` para a pasta Downloads do usuário student no bastion. Ajuste o caminho se o download foi salvo em outro local. Não execute como root.

Antes, preserve alterações locais, inclusive as de uma entrega incremental ainda não enviada. A importação abaixo exige uma árvore de trabalho limpa para que você possa comparar e desfazer pelo Git. Commitar alterações locais não exige enviá-las imediatamente ao GitHub.

```bash
cd ~/rhcsa-ex200-v10-lab
git status --short
```

Depois que não houver alterações pendentes, execute este bloco. Ele cria uma branch própria, extrai o pacote na raiz e interrompe em caso de falha:

```bash
(
  set -Eeuo pipefail
  cd ~/rhcsa-ex200-v10-lab
  test -z "$(git status --porcelain)"
  git switch -c docs/setup-kvm
  tar --no-same-owner -xzf "$HOME/Downloads/rhcsa-ex200-v10-lab-docs-kvm-v3.tar.gz" -C .
  git diff --check
  git diff -- README.md docs/setup/README.md
  git status --short
)
```

Se a branch já existir, use um novo nome ou continue nela após conferir seu estado; não remova a branch anterior automaticamente. O arquivo tar não contém `.git`, credenciais, inventário pessoal ou bytecode Python.

## Revisar e enviar

Abra `README.md` e navegue pelos links dos oito guias. Confira a rede, os caminhos e as particularidades da sua instalação. Os comandos de criação de VMs são para quem começa do zero, não para recriar automaticamente as suas VMs existentes.

```bash
cd ~/rhcsa-ex200-v10-lab
git add README.md README-DOCS-SETUP.md docs/setup
git diff --cached --check
git diff --cached --stat
git commit -m "docs: add KVM setup guide and linked onboarding steps"
git push -u origin docs/setup-kvm
```

Abra um Pull Request da branch `docs/setup-kvm` para a branch principal do repositório e revise a mudança. Depois de mesclar, a home pública mostrará os novos links. O push requer a sua autenticação GitHub já configurada; este pacote não altera o remote nem contém token.

Os arquivos devem ser versionados **extraídos**, para o GitHub renderizar a home e os guias. O `.tar.gz` é o meio de entrega; commitar apenas o arquivo comprimido não atualiza a home.

## Verificação realizada na geração

- caminhos de entrada do tar sem diretórios absolutos ou `..`;
- links relativos da documentação conferidos com a estrutura do projeto;
- exemplos alinhados ao inventário e ao instalador do CLI existentes;
- somente documentação modificada.

Os comandos KVM, instalação RHEL, SSH e Ansible precisam ser validados no host/VMs reais. Eles não foram executados sobre as suas máquinas durante a geração deste pacote.
