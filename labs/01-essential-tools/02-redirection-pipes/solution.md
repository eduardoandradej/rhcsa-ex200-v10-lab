# Solução possível — obj01-02

```bash
cd /home/student/rhcsa-lab/obj01-02

bin/stream-demo > output/stdout.log 2> output/stderr.log
bin/stream-demo > output/combined.log 2>&1

bin/append-demo >> output/append.log
bin/append-demo >> output/append.log

cat input/services.txt | sort | uniq > output/services-unique.txt
grep 'active' input/status.txt | wc -l > output/active-count.txt
```

Outras soluções que produzam o mesmo estado final são válidas.
