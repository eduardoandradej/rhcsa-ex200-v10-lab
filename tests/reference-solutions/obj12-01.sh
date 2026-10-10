#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -Eeuo pipefail -s' <<'EOS'
sudo groupadd ops12
sudo useradd -m -s /bin/bash -G ops12 analyst12
sudo chage -m 2 -M 45 -W 7 analyst12
sudo mkdir -p /srv/team12
sudo chown root:ops12 /srv/team12
sudo chmod 2770 /srv/team12
sudo setfacl -m u:student:rwx /srv/team12
sudo touch /srv/team12/alpha.txt /srv/team12/beta.txt
sudo chown root:ops12 /srv/team12/alpha.txt /srv/team12/beta.txt
sudo chmod 0660 /srv/team12/alpha.txt /srv/team12/beta.txt
sudo tee /usr/local/bin/count-team12 >/dev/null <<'EOF'
#!/bin/bash
set -Eeuo pipefail
[[ $# -eq 1 && -d "$1" ]] || exit 2
find "$1" -maxdepth 1 -type f -printf '.' | wc -c
EOF
sudo chmod 0755 /usr/local/bin/count-team12
cd /home/student/rhcsa-lab/obj12-01
id analyst12 > output/id.txt
sudo chage -l analyst12 > output/chage.txt
getfacl -p /srv/team12 > output/acl.txt
/usr/local/bin/count-team12 /srv/team12 > output/count.txt
EOS
