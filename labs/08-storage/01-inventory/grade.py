#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json, subprocess
root=Path("/home/student/rhcsa-lab/obj08-01/output")
def t(n):
 p=root/n
 return p.read_text(errors="replace") if p.is_file() else ""
checks=[
 {"label":"lsblk identifica discos scratch","pass":all(x in t("lsblk.txt") for x in ["vdb","vdc","vdd","vde"]),"hint":"Salve lsblk com os campos pedidos."},
 {"label":"inventário preserva disco de sistema","pass":"vda" in t("lsblk.txt") and "rhel_servera-root" in t("lsblk.txt"),"hint":"O inventário deve mostrar vda e o LV root."},
 {"label":"estado LVM foi salvo","pass":"rhel_servera" in t("pvs.txt") and "rhel_servera" in t("vgs.txt") and "rhel_servera" in t("lvs.txt"),"hint":"Salve pvs/vgs/lvs."},
 {"label":"findmnt e parted foram registrados","pass":"/" in t("findmnt.txt") and len(t("parted-vdb.txt"))>0,"hint":"Salve findmnt e a inspeção do vdb."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj08-01","checks":checks,"score":score},ensure_ascii=False))
"""

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--json", action="store_true")
    p.parse_args()
    result = json_from_remote_python("servera", REMOTE_CHECKER)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["score"] == 100 else 1

if __name__ == "__main__":
    raise SystemExit(main())
