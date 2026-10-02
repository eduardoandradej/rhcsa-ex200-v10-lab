No `servera`, configure manualmente o arquivo
`/etc/yum.repos.d/rhcsa-custom.repo` com:

- ID: `rhcsa-custom`
- name: `RHCSA Custom Repository`
- baseurl: `file:///var/lib/rhcsa-lab/obj03/repos/base`
- enabled: `1`
- gpgcheck: `0`

Depois:

1. Limpe/metadados do DNF conforme necessário.
2. Confirme que `rhcsa-custom` aparece habilitado em `dnf repolist`.
3. Confirme que `rhcsa-toolkit` pode ser listado a partir desse repositório.

Não instale o pacote.
