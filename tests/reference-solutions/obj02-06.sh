#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'sudo bash -Eeuo pipefail -s' <<'EOS'
usermod -aG opsadmin svcadmin
printf '%s\n' '%opsadmin ALL=(root) NOPASSWD: /usr/bin/id, /usr/bin/whoami' > /etc/sudoers.d/opsadmin
chmod 0440 /etc/sudoers.d/opsadmin
visudo -cf /etc/sudoers.d/opsadmin
runuser -u svcadmin -- sudo -n /usr/bin/id -u
EOS
