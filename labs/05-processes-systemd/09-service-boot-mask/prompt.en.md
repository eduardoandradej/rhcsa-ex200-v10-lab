On `servera`, the lab installed:

```text
rhcsa-boot.service
rhcsa-blocked.service
```

Initial state:

- `rhcsa-boot`: inactive and disabled;
- `rhcsa-blocked`: active and enabled.

Tasks:

1. Configure `rhcsa-boot.service` to start at boot **and** leave it active now.
2. Save dependencies for `rhcsa-boot.service` to
   `output/boot-dependencies.txt`.
3. Stop `rhcsa-blocked.service`.
4. Disable `rhcsa-blocked.service`.
5. Mask `rhcsa-blocked.service`.

Final state:

```text
rhcsa-boot.service      active + enabled
rhcsa-blocked.service   inactive + masked
```
