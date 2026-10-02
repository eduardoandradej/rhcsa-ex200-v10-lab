# Entrega 5 — Objective 05 Processes, Scheduling, Tuning & systemd

Version: `1.1.0`

## New labs

- obj05-01 — Identificar processos, PIDs e estados
- obj05-02 — Controlar jobs em foreground e background
- obj05-03 — Controlar processos com sinais
- obj05-04 — Identificar e encerrar processos intensivos
- obj05-05 — Ajustar prioridade com nice e renice
- obj05-06 — Gerenciar perfis de ajuste com TuneD
- obj05-07 — Identificar units e estados do systemd
- obj05-08 — Start, restart e reload de serviço
- obj05-09 — Enable, disable, mask e dependências
- obj05-10 — Desafio integrado de processos e systemd

## Run

```bash
bash tests/release-gate.sh
bash tests/integration-objective05.sh
```

After Objective 05 passes:

```bash
bash tests/integration-reference.sh
```

The full regression now covers **44 labs** and automatically prepares
Objective 03 and Objective 05 infrastructure when run without arguments.
