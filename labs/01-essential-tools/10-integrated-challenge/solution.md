# Solução possível — obj01-10

Uma solução de referência:

```bash
cd /home/student/rhcsa-lab/obj01-10

mkdir -p work/{reports,logs,links,archive}

cp input/report.txt work/reports/final-report.txt

grep -F '|prod|active|' input/systems.txt   > work/reports/prod-active.txt

grep -E 'WARN|ERROR' input/events.log   > work/logs/alerts.log

ssh student@serverb 'hostname -f'   > work/reports/remote-host.txt

sed -i 's/STATUS=PENDING/STATUS=READY/'   work/reports/final-report.txt

chmod 640 work/reports/final-report.txt
chmod 750 work/reports

ln work/reports/final-report.txt   work/links/report.hard

ln -s ../logs/alerts.log   work/links/alerts.current

(
  cd work
  tar -czf archive/evidence.tar.gz reports logs
)

man -w chmod > work/reports/chmod-manpath.txt
```
