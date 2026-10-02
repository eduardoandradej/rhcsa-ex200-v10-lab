# Solução possível — obj01-01

Uma solução possível, executada como `student` no `servera`:

```bash
cd /home/student/rhcsa-lab/obj01-01

mkdir -p workspace/{reports,images,notes}

cp input/report-*.txt workspace/reports/
mv input/image-*.jpg workspace/images/
mv input/notes-old.txt workspace/notes/notes-final.txt

touch workspace/notes/note-{1..3}.txt

rm input/*.tmp
```

Valide com:

```bash
exit
lab grade obj01-01
```

O grader avalia o estado final. Outros comandos que produzam o mesmo estado também são válidos.
