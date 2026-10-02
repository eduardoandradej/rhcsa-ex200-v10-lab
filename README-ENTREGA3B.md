# Entrega 3B — Objective 03 RPM, DNF & Repositories

Versão: `0.9.0`

## Novos labs

- `obj03-01` — Consultar a base RPM instalada
- `obj03-02` — Inspecionar e extrair um arquivo RPM
- `obj03-03` — Descobrir software com DNF
- `obj03-04` — Instalar e remover pacotes com DNF
- `obj03-05` — Configurar um repositório DNF
- `obj03-06` — Atualizar pacote por repositório de errata
- `obj03-07` — Auditar transações com DNF history
- `obj03-08` — Desafio integrado de gerenciamento de software

## Preparação determinística

O wrapper de integração executa automaticamente:

```bash
ansible-playbook ansible/prepare-objective03.yml
```

Esse playbook instala somente dependências de infraestrutura do laboratório
(`rpm-build`, `createrepo_c`, `cpio`, `dnf-plugins-core`) e constrói pequenos
RPMs originais para o exercício.

## Validação

```bash
bash tests/release-gate.sh
bash tests/integration-objective03.sh
```

Depois que os oito labs passarem:

```bash
bash tests/integration-reference.sh
```
