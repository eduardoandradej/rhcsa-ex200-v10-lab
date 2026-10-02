```bash
cd /home/student/rhcsa-lab/obj04-03

cat > checkcmd.sh <<'EOF'
#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: checkcmd.sh COMMAND" >&2
    exit 2
fi

if path=$(command -v "$1"); then
    echo "FOUND:$1:$path"
else
    echo "NOTFOUND:$1"
    exit 1
fi
EOF

chmod +x checkcmd.sh
```
