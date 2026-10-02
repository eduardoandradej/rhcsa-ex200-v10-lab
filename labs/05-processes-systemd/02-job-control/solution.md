Execute em **uma mesma shell**:

```bash
cd /home/student/rhcsa-lab/obj05-02
set -m

./assets/job-alpha &
echo $! > output/alpha.pid

./assets/job-beta &
echo $! > output/beta.pid

kill -s STOP %1

jobs -l > output/jobs.txt

ps -o pid=,stat=,args= \
  -p "$(cat output/alpha.pid),$(cat output/beta.pid)" \
  > output/processes.txt
```
