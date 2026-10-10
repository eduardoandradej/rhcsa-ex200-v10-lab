# Entrega 9 — OBJ09 / v1.5.0

Esta entrega adiciona o Objective 09 — Boot, GRUB & Recovery.

Aplicar sobre a linha estável v1.4.13.

Após aplicar:

```bash
cd ~/rhcsa-ex200-v10-lab
lab --version
bash tests/validate-obj09.sh
bash tests/integration-objective09.sh
```

Esperado:

```text
lab 1.5.0
OBJ09 VALIDATION: PASS
OBJ09 AUTOMATED INTEGRATION: PASS
```

`obj09-04` e `obj09-06` são drills de console `manual-only`. A justificativa
técnica e a estratégia de prática RHEL 10 estão em
`docs/OBJ09-BOOT-RECOVERY.md`.
