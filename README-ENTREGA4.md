# Entrega 4 — Objective 04 Simple Shell Scripts

Versão: `1.0.0`

## Novos labs

- `obj04-01` — Parâmetros posicionais e validação de entrada
- `obj04-02` — Condições com test e colchetes
- `obj04-03` — Decisões a partir do status de comandos
- `obj04-04` — Processar saída de comandos em um script
- `obj04-05` — Loop sobre argumentos da linha de comando
- `obj04-06` — Loop sobre entrada de arquivo
- `obj04-07` — Relatório de usuários com loop e saída de comandos
- `obj04-08` — Desafio integrado de shell scripting

## Foco de exame

O bloco foi desenhado estritamente em torno do objetivo EX200 de criar
scripts shell simples:

- condicionais;
- loops;
- parâmetros posicionais;
- processamento de saída de comandos.

Não transforma o projeto em um curso de Bash avançado.

## Validação

```bash
bash tests/release-gate.sh
bash tests/integration-objective04.sh
```

Após os oito labs passarem:

```bash
bash tests/integration-reference.sh
```

A regressão global passa a cobrir **34 labs**.
