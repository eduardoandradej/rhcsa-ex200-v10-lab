#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj04-02
cat > checkpath.sh <<'EOF'
#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Usage: checkpath.sh PATH" >&2
    exit 2
fi
if [ -f "$1" ]; then
    echo "FILE:$1"
elif [ -d "$1" ]; then
    echo "DIRECTORY:$1"
else
    echo "MISSING:$1"
    exit 1
fi
EOF
chmod +x checkpath.sh
EOS
