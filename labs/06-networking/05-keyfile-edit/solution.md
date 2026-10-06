Uma solução possível:
```bash
sudo python3 - <<'PY'
from pathlib import Path
p=Path('/etc/NetworkManager/system-connections/ex200-keyfile.nmconnection')
s=p.read_text()
s=s.replace('address1=10.66.5.10/24','address1=10.66.5.10/24\naddress2=10.66.5.110/24')
p.write_text(s)
PY
sudo nmcli con reload
sudo nmcli con up ex200-keyfile
ip -4 -br addr show ex200a > /home/student/rhcsa-lab/obj06-05/output/runtime.txt
```