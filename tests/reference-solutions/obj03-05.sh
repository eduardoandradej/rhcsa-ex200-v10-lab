#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'sudo bash -Eeuo pipefail -s' <<'EOS'
cat > /etc/yum.repos.d/rhcsa-custom.repo <<'EOF'
[rhcsa-custom]
name=RHCSA Custom Repository
baseurl=file:///var/lib/rhcsa-lab/obj03/repos/base
enabled=1
gpgcheck=0
EOF
dnf clean metadata >/dev/null
dnf --disablerepo='*' --enablerepo=rhcsa-custom list rhcsa-toolkit >/dev/null
EOS
