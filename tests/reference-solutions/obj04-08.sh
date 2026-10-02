#!/usr/bin/env bash
set -Eeuo pipefail
ssh serverb 'bash -Eeuo pipefail -s' <<'EOS'
cd /home/student/rhcsa-lab/obj04-08
cat > account-audit.sh <<'EOF'
#!/bin/bash
if [ "$#" -ne 2 ]; then
    echo "Usage: account-audit.sh INPUT_FILE OUTPUT_FILE" >&2
    exit 2
fi

input=$1
output=$2

if [ ! -f "$input" ]; then
    echo "MISSING-FILE:$input"
    exit 1
fi

host=$(hostname -s)
total=0
found=0
missing=0

echo "HOST=$host" > "$output"

for user in $(cat "$input"); do
    [ -z "$user" ] && continue
    total=$(( total + 1 ))

    if entry=$(getent passwd "$user"); then
        uid=$(echo "$entry" | cut -d: -f3)

        if [ "$uid" -eq 0 ]; then
            type=PRIVILEGED
        elif [ "$uid" -lt 1000 ]; then
            type=SYSTEM
        else
            type=REGULAR
        fi

        echo "USER:$user:UID=$uid:TYPE=$type" >> "$output"
        found=$(( found + 1 ))
    else
        echo "USER:$user:MISSING" >> "$output"
        missing=$(( missing + 1 ))
    fi
done

echo "SUMMARY:TOTAL=$total:FOUND=$found:MISSING=$missing" >> "$output"
EOF
chmod +x account-audit.sh
EOS
