# Entrega 2A — Python lab CLI

Esta entrega adiciona:

- `lab status`
- `lab list`
- catálogo inicial do Objetivo 01
- wrapper `bin/lab`
- instalador em `bootstrap/10-install-lab-cli.sh`

## Instalação

Mescle estes arquivos no repositório do bastion e execute:

```bash
cd ~/rhcsa-ex200-v10-lab
./bootstrap/10-install-lab-cli.sh
source ~/.bashrc
```

## Testes

```bash
lab --version
lab status
lab list
lab list --objective essential
```

## Observação

Os 10 itens do Objetivo 01 estão inicialmente marcados como `catalog-only`.
Eles entram no catálogo agora, mas setup, enunciado, grade e cleanup serão implementados nas próximas entregas.
