## Integrated challenge — RPM/DNF/Repositories

On `serverb`, work in `/home/student/rhcsa-lab/obj03-08`.

1. Create `/etc/yum.repos.d/rhcsa-system.repo` containing:
   - `[rhcsa-system-base]`
     - `baseurl=file:///var/lib/rhcsa-lab/obj03/repos/base`
     - enabled
     - `gpgcheck=0`
   - `[rhcsa-system-errata]`
     - `baseurl=file:///var/lib/rhcsa-lab/obj03/repos/errata`
     - initially disabled
     - `gpgcheck=0`
2. Install `rhcsa-system` version `1.0-1` from the base repository.
3. Inspect local RPM `assets/rhcsa-local-1.0-1.noarch.rpm` with RPM and
   save its information to `output/local-rpm-info.txt`.
4. Install that local RPM with DNF.
5. Enable the errata repository and upgrade `rhcsa-system` to `2.0-1`.
6. At the end, persistently disable both custom repositories.
7. Identify the most recent DNF transaction involving `rhcsa-system` and save
   `dnf history info <ID>` to `output/history.txt`.

Expected final state:

- `rhcsa-system-2.0-1` installed;
- `rhcsa-local-1.0-1` installed;
- both custom repositories disabled.
