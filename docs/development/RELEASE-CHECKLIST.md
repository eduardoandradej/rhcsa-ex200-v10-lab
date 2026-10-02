# Release checklist

Antes de publicar uma entrega:

```bash
bash tests/release-gate.sh
```

O gate valida:

- sintaxe dos módulos Python;
- sintaxe de todos os graders;
- metadados YAML do catálogo;
- sintaxe dos playbooks `setup.yml` e `finish.yml`;
- inicialização do CLI e descoberta do catálogo.

Para laboratórios novos, ainda é obrigatório executar ao menos uma vez o ciclo real:

```text
lab start -> resolução -> lab grade -> lab finish
```

O release só deve ser publicado depois do ciclo real atingir `PASS`.
