```bash
cd /home/student/rhcsa-lab/obj05-05

nice -n 12 ./assets/nice-start &
echo $! > output/nice-start.pid

./assets/nice-change &
echo $! > output/nice-change.pid

renice -n 7 -p "$(cat output/nice-change.pid)"

ps -o pid=,ni=,stat=,args= \
  -p "$(cat output/nice-start.pid),$(cat output/nice-change.pid)" \
  > output/priorities.txt
```
