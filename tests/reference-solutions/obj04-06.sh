#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj04-06
cat > fileloop.sh <<'EOF'
#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Usage: fileloop.sh FILE" >&2
    exit 2
fi
if [ ! -f "$1" ]; then
    echo "MISSING-FILE:$1"
    exit 1
fi
for item in $(cat "$1"); do
    [ -n "$item" ] && echo "ITEM:$item"
done
EOF
chmod +x fileloop.sh
EOS
