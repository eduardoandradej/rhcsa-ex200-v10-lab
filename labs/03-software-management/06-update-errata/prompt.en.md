On `servera`, `rhcsa-update-demo-1.0-1` is already installed.

Two repositories exist:

- `rhcsa-base` — enabled, contains `1.0-1`;
- `rhcsa-errata` — disabled, contains `2.0-1`.

Perform these tasks:

1. Persistently enable `rhcsa-errata`.
2. Upgrade **only** `rhcsa-update-demo` to the latest available version.
3. Verify the installed version with RPM.
4. At the end, persistently disable **both custom repositories**.

Do not remove the upgraded package.
