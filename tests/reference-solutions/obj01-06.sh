#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -s' <<'EOS'
cat > /home/student/rhcsa-lab/obj01-06/app.conf <<'EOF'
# RHCSA training application
environment=production
workers=8
logging=verbose
port=8080
EOF
cat > /home/student/rhcsa-lab/obj01-06/notes.txt <<'EOF'
review completed
configuration updated
ready for validation
EOF
EOS
