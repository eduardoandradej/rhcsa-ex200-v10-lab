# Entrega 2D — redirection, pipes, grep e regex

Versão do CLI: `0.5.0`

Esta entrega:

- torna `obj01-02` executável;
- torna `obj01-03` executável;
- centraliza execução Python remota em `labctl/remote.py`;
- mantém o grader do `obj01-01` sobre a mesma infraestrutura reutilizável;
- adiciona `tests/release-gate.sh`.

## Ciclo de validação

```bash
bash tests/release-gate.sh

lab start obj01-02
# resolver no servera
lab grade obj01-02
lab finish obj01-02

lab start obj01-03
# resolver no servera
lab grade obj01-03
lab finish obj01-03
```
