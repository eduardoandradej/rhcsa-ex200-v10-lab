#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python
REMOTE_CHECKER = r"""
from pathlib import Path
import json
r=Path("/home/student/rhcsa-lab/obj07-05/output")
def t(n):
 p=r/n; return p.read_text(errors="replace") if p.is_file() else ""
tag=t("tag.txt"); warn=t("warning.txt"); unit=t("unit.txt")
checks=[
 {"label":"filtro por tag encontrou eventos","pass":"OBJ07-JOURNAL-INFO" in tag and "OBJ07-JOURNAL-WARNING" in tag,"hint":"Use -t e --since."},
 {"label":"warning preservado","pass":"OBJ07-JOURNAL-WARNING" in warn,"hint":"Use -p warning."},
 {"label":"info excluído do warning","pass":"OBJ07-JOURNAL-INFO" not in warn,"hint":"Combine filtros."},
 {"label":"filtro por unit encontrou evento","pass":"OBJ07-UNIT-EVENT" in unit,"hint":"Use _SYSTEMD_UNIT."}]
score=round(sum(c["pass"] for c in checks)/len(checks)*100); print(json.dumps({"lab_id":"obj07-05","checks":checks,"score":score},ensure_ascii=False))
"""
def main():
    p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
    result=json_from_remote_python("servera",REMOTE_CHECKER)
    print(json.dumps(result,ensure_ascii=False))
    return 0 if result["score"]==100 else 1
if __name__ == "__main__": raise SystemExit(main())
