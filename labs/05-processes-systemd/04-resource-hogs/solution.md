```bash
cd /home/student/rhcsa-lab/obj05-04

cpid=$(cat /run/rhcsa-cpu-hog.pid)
mpid=$(cat /run/rhcsa-mem-hog.pid)

ps -o pid=,%cpu=,%mem=,stat=,args= -p "$cpid" > output/cpu-before.txt
ps -o pid=,%cpu=,%mem=,stat=,args= -p "$mpid" > output/memory-before.txt

kill -s TERM "$cpid"
kill -s TERM "$mpid"
```
