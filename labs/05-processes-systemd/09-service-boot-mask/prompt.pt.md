No `servera`, o laboratório instalou:

```text
rhcsa-boot.service
rhcsa-blocked.service
```

Estado inicial:

- `rhcsa-boot`: inativo e desabilitado;
- `rhcsa-blocked`: ativo e habilitado.

Tarefas:

1. Configure `rhcsa-boot.service` para iniciar no boot **e** deixe-o ativo agora.
2. Grave as dependências de `rhcsa-boot.service` em
   `output/boot-dependencies.txt`.
3. Pare `rhcsa-blocked.service`.
4. Desabilite `rhcsa-blocked.service`.
5. Mascare `rhcsa-blocked.service`.

Estado final:

```text
rhcsa-boot.service      active + enabled
rhcsa-blocked.service   inactive + masked
```
