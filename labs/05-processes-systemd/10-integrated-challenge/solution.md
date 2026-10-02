```bash
cd /home/student/rhcsa-lab/obj05-10

rogue=$(cat /run/rhcsa-rogue-cpu.pid)

ps -o pid=,%cpu=,%mem=,ni=,stat=,args= \
  -p "$rogue" > output/rogue-before.txt

kill -s TERM "$rogue"

nice -n 10 ./assets/batch-worker &
echo $! > output/batch.pid

sudo systemctl enable --now rhcsa-api.service

sudo systemctl stop rhcsa-legacy.service
sudo systemctl disable rhcsa-legacy.service
sudo systemctl mask rhcsa-legacy.service

sudo tuned-adm profile balanced
tuned-adm active > output/tuned-active.txt
```
