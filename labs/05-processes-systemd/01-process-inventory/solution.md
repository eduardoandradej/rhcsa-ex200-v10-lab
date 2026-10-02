```bash
cd /home/student/rhcsa-lab/obj05-01

ps -o pid=,ppid=,stat=,ni=,args= \
  -p "$(cat /run/rhcsa-proc-sleeper.pid)" > output/sleeper.txt

ps -o pid=,ppid=,stat=,ni=,args= \
  -p "$(cat /run/rhcsa-proc-stopped.pid)" > output/stopped.txt
```
