```bash
cd /home/student/rhcsa-lab/obj04-04

cat > sysreport.sh <<'EOF'
#!/bin/bash

host=$(hostname -s)
kernel=$(uname -r)
bash_path=$(command -v bash)
user_count=$(getent passwd | wc -l)

echo "HOSTNAME=$host"
echo "KERNEL=$kernel"
echo "BASH_PATH=$bash_path"
echo "USER_COUNT=$user_count"
EOF

chmod +x sysreport.sh
```
