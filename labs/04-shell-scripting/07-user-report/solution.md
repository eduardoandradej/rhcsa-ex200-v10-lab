```bash
cd /home/student/rhcsa-lab/obj04-07

cat > userreport.sh <<'EOF'
#!/bin/bash

if [ "$#" -eq 0 ]; then
    echo "NO-USERS"
    exit 1
fi

for user in "$@"; do
    if entry=$(getent passwd "$user"); then
        uid=$(echo "$entry" | cut -d: -f3)
        home=$(echo "$entry" | cut -d: -f6)
        shell=$(echo "$entry" | cut -d: -f7)
        echo "USER:$user:UID=$uid:HOME=$home:SHELL=$shell"
    else
        echo "USER:$user:MISSING"
    fi
done
EOF

chmod +x userreport.sh
```
