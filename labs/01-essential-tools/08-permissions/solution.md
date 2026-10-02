# Solução possível — obj01-08

```bash
cd /home/student/rhcsa-lab/obj01-08

chmod 640 data/report.txt
chmod 750 data/scripts
chmod u+x data/scripts/backup.sh

umask 0027
touch generated/new-file.txt
mkdir generated/new-dir
```
