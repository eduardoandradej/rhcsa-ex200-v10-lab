```bash
cd /home/student/rhcsa-lab/obj05-08

sudo systemctl start rhcsa-control.service
systemctl show -p MainPID --value rhcsa-control.service > output/start.pid

sudo systemctl restart rhcsa-control.service
systemctl show -p MainPID --value rhcsa-control.service > output/restart.pid

sudo systemctl reload rhcsa-control.service
systemctl show -p MainPID --value rhcsa-control.service > output/reload.pid
```
