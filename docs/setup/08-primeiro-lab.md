# 08 — Primeiro exercício

[Índice](README.md) · [Home](../../README.md) · [Anterior](07-baseline.md)

**Onde executar:** comandos `lab` no bastion; solução manual no alvo indicado pelo enunciado.

```bash
cd ~/rhcsa-ex200-v10-lab
lab status
lab list
lab show obj01-01
lab start obj01-01
ssh servera
```

Dentro de servera, leia o enunciado e trabalhe em `/home/student/rhcsa-lab/obj01-01`. Resolva as tarefas manualmente. Ao terminar:

```bash
exit
lab grade obj01-01
```

A nota valida o estado final. Se houver critérios pendentes, volte ao alvo, corrija e execute `lab grade obj01-01` novamente. Ao encerrar a prática:

```bash
lab finish obj01-01
lab status
```

Execute `finish` apenas quando quiser limpar o exercício. Inicie um único exercício por vez. Itens `catalog-only` aparecem no catálogo, mas ainda não podem ser iniciados; use apenas itens `ready`.

A disponibilidade real vem de `lab list`. Novas entregas podem acrescentar exercícios sem alterar o roteiro de instalação. Este pacote de documentação não incorpora nem substitui as entregas 2C/2D/2E de código.

A limpeza de cada exercício tem o escopo definido em `finish.yml`; para recuperar a VM completa, consulte a etapa de baseline. Os enunciados e soluções públicos são autorais; este projeto não é o ambiente oficial da Red Hat.

**Resultado esperado:** conseguir iniciar, resolver, avaliar e finalizar o primeiro cenário, deixando o ambiente pronto para a próxima prática.

[Índice](README.md) · [Home](../../README.md) · [Anterior](07-baseline.md)
