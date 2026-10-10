No `servera`, trabalhe em `/home/student/rhcsa-lab/obj10-01`.

Sem alterar a configuração:

1. Grave o modo SELinux atual em `output/getenforce.txt`.
2. Grave o resumo do SELinux em `output/sestatus.txt`.
3. Grave o contexto SELinux do processo `sshd` em `output/sshd-process.txt`.
4. Grave o contexto SELinux de `/etc/ssh/sshd_config` em
   `output/sshd-config.txt`.
5. Grave as customizações locais de contextos de arquivos em
   `output/fcontext-local.txt`.

O objetivo é distinguir modo SELinux, contexto de processo, contexto de arquivo
e política local persistente.
