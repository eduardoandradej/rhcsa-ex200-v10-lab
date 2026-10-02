#!/usr/bin/env bash
set -Eeuo pipefail

ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj01-04

# -n is critical here: this script itself is being fed to bash through stdin.
# Without -n, the nested ssh client can consume the remaining heredoc.
ssh -n -o BatchMode=yes student@serverb 'hostname -f' > remote-host.txt
ssh -n -o BatchMode=yes student@serverb 'whoami' > remote-user.txt

sudo -u labuser bash -c 'whoami > /home/labuser/switch-user.txt'
EOS
