On `servera`, manually configure
`/etc/yum.repos.d/rhcsa-custom.repo` with:

- ID: `rhcsa-custom`
- name: `RHCSA Custom Repository`
- baseurl: `file:///var/lib/rhcsa-lab/obj03/repos/base`
- enabled: `1`
- gpgcheck: `0`

Then:

1. Refresh DNF metadata as needed.
2. Confirm `rhcsa-custom` is enabled in `dnf repolist`.
3. Confirm `rhcsa-toolkit` can be listed from that repository.

Do not install the package.
