# Hotfix 0.9.1 — obj03-08 DNF history

## Causa

O arquivo `output/history.txt` era criado com:

```bash
dnf history list rhcsa-system
```

Essa saída lista as transações correspondentes, mas não é um formato estável
para exigir que o nome completo do pacote apareça literalmente em cada linha.
O grader, por outro lado, exigia a string `rhcsa-system`.

Resultado: o estado do pacote e dos repositórios estava correto, mas o último
check retornava FAIL.

## Correção

O exercício agora segue a mesma estratégia robusta do `obj03-07`:

1. `dnf history list rhcsa-system` localiza a transação;
2. `dnf history info <ID>` grava os detalhes em `output/history.txt`;
3. o grader valida os detalhes da transação.

Isso também fica mais próximo da prática do RH199, que usa `dnf history`
seguido de `dnf history info <ID>`.

## Reteste

```bash
bash tests/integration-reference.sh obj03-08
```

Se passar, o Objective 03 está fechado: 8/8.
