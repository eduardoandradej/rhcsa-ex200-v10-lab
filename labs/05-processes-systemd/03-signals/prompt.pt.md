No `servera`, existem três processos de treinamento:

```text
rhcsa-signal-alpha   inicialmente executando
rhcsa-signal-beta    inicialmente executando
rhcsa-signal-gamma   inicialmente parado
```

Os PIDs estão em `/run/rhcsa-signal-*.pid`.

Faça o seguinte usando **nomes de sinais**:

1. envie `SIGSTOP` para `alpha`;
2. envie `SIGTERM` para `beta`;
3. envie `SIGCONT` para `gamma`.

Estado final:

- `alpha` existe e está em `T`;
- `beta` não existe mais;
- `gamma` existe e não está em `T`.

Não use `SIGKILL` neste exercício.
