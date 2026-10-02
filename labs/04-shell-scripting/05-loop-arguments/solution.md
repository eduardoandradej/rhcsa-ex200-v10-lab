```bash
cd /home/student/rhcsa-lab/obj04-05

cat > argloop.sh <<'EOF'
#!/bin/bash

if [ "$#" -eq 0 ]; then
    echo "NO-ARGS"
    exit 1
fi

for item in "$@"; do
    echo "ARG:$item"
done
EOF

chmod +x argloop.sh
```
