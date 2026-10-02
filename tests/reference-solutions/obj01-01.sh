#!/usr/bin/env bash
set -Eeuo pipefail
ssh servera 'bash -s' <<'EOS'
cd /home/student/rhcsa-lab/obj01-01
mkdir -p workspace/{reports,images,notes}
cp input/report-*.txt workspace/reports/
mv input/image-*.jpg workspace/images/
mv input/notes-old.txt workspace/notes/notes-final.txt
touch workspace/notes/note-{1..3}.txt
rm -f input/*.tmp
EOS
