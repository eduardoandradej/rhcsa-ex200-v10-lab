# Solução possível — obj04-01

```bash
cd /home/student/rhcsa-lab/obj04-01

cat > greet.sh <<'EOF'
#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: greet.sh USER ROLE" >&2
    exit 2
fi

echo "USER=$1 ROLE=$2"
EOF

chmod +x greet.sh
```
