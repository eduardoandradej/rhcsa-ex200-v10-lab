# Entrega 2C — primeiro laboratório executável

Esta entrega implementa o ciclo completo do `obj01-01`:

```bash
lab start obj01-01
lab grade obj01-01
lab finish obj01-01
```

Também adiciona estado local em `.state/active.json`.

## Teste sugerido

```bash
lab status
lab start obj01-01

ssh servera
cd /home/student/rhcsa-lab/obj01-01
# resolva o exercício
exit

lab grade obj01-01
lab finish obj01-01
lab status
```

Os demais exercícios continuam como `catalog-only`.

## Filosofia do grader

O grader valida o estado final, não a sequência exata de comandos usada pelo estudante.
