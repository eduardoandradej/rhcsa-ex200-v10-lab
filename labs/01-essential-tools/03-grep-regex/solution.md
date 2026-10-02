# Solução possível — obj01-03

```bash
cd /home/student/rhcsa-lab/obj01-03

grep -E '^SRV-[0-9]{3}\|' input/systems.txt > output/servers.txt
grep -E '\|web[^|]*\|' input/systems.txt > output/web-hosts.txt
grep -F '|prod|active|' input/systems.txt > output/prod-active.txt
grep -E 'WARN|ERROR' input/events.log > output/alerts.log
grep -E '\.21$' input/systems.txt > output/ip-ending-21.txt
```

Outras soluções que produzam o mesmo estado final são válidas.
