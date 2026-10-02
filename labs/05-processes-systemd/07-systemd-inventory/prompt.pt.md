No `servera`, trabalhe em `/home/student/rhcsa-lab/obj05-07`.

Sem modificar serviços, gere:

1. `output/services.txt`
   - todas as service units carregadas, ativas e inativas.
2. `output/unit-files.txt`
   - todos os arquivos de units do tipo service.
3. `output/sshd-active.txt`
   - resultado de `systemctl is-active sshd.service`.
4. `output/sshd-enabled.txt`
   - resultado de `systemctl is-enabled sshd.service`.
5. `output/chronyd-status.txt`
   - `systemctl status chronyd.service` sem pager.

O objetivo é distinguir estado de runtime (`active`) de configuração de boot (`enabled`).
