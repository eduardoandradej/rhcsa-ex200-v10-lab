# Hotfix 0.6.2

`obj01-05` agora provisiona automaticamente o utilitário `bzip2` quando ele
não está presente no RHEL mínimo.

O pacote é obtido da mídia local RHEL 9.8 já montada no bastion em:

```text
/mnt/rhel9dvd
```

Com isso, o laboratório não depende de registro RHSM nem de repositório
externo para instalar essa dependência.

Validação:

```bash
lab --version
bash tests/release-gate.sh
bash tests/integration-reference.sh obj01-05 obj01-06 obj01-07
```
