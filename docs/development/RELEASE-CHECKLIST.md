# Release checklist

O projeto usa dois níveis de validação.

## 1. Gate estático

```bash
bash tests/release-gate.sh
```

Valida sintaxe Python, metadados YAML, contrato dos labs `ready`, sintaxe Ansible e smoke test do CLI.

## 2. Integração de referência

```bash
bash tests/integration-reference.sh
```

Esse teste:

1. executa `lab start`;
2. aplica uma solução de referência automatizada;
3. exige `Score: 100%`;
4. executa `lab finish`;
5. repete o ciclo para os laboratórios selecionados.

Para testar somente alguns labs:

```bash
bash tests/integration-reference.sh obj01-04 obj01-05 obj01-06 obj01-07
```

A solução de referência existe para validar a engenharia do lab. O fluxo normal do estudante continua sendo manual.
