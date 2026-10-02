#!/usr/bin/env bash
set -Eeuo pipefail
ssh serverb 'sudo bash -Eeuo pipefail -s' <<'EOS'
sed -ri 's/^[[:space:]]*PASS_MAX_DAYS[[:space:]]+.*/PASS_MAX_DAYS 30/' /etc/login.defs
groupadd -g 35050 consultantsx
printf '%s\n' '%consultantsx ALL=(ALL) ALL' > /etc/sudoers.d/consultantsx
chmod 0440 /etc/sudoers.d/consultantsx
visudo -cf /etc/sudoers.d/consultantsx
for u in consultx1 consultx2 consultx3; do
  useradd -G consultantsx "$u"
done
printf 'consultx1:redhat\nconsultx2:redhat\nconsultx3:redhat\n' | chpasswd
exp="$(date -d '+90 days' +%F)"
for u in consultx1 consultx2 consultx3; do
  chage -E "$exp" -d 0 "$u"
done
chage -M 15 consultx2
EOS
