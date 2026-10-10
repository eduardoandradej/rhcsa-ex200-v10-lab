Referência prática:

```text
GRUB: adicionar temporariamente
systemd.unit=emergency.target
```

No shell de manutenção, quando `/` estiver somente leitura e for necessário
editar configuração:

```bash
mount -o remount,rw /
```

A alteração feita no editor do GRUB não deve ser persistida. Ao finalizar,
retorne ao boot normal.
