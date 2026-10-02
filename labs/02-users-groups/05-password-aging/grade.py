#!/usr/bin/env python3
import argparse,json
from labctl.remote import json_from_remote_python
REMOTE_CHECKER=r"""
import json, subprocess
def shadow(name):
    p=subprocess.run(["sudo","-n","getent","shadow",name],text=True,stdout=subprocess.PIPE)
    return p.stdout.rstrip("\n").split(":") if p.returncode==0 else None
def epoch_days_plus(days):
    p=subprocess.run(["date","-d",f"+{days} days","+%s"],text=True,stdout=subprocess.PIPE)
    return int(p.stdout.strip())//86400
a=shadow("aginguser1"); b=shadow("aginguser2")
password_ok=lambda x: bool(x and x[1] and not x[1].startswith(("!","*")))
checks=[
 {"label":"aginguser1 possui senha definida","pass":password_ok(a),"hint":"Defina uma senha para aginguser1."},
 {"label":"aginguser1 possui política 2/45/7/5","pass":bool(a and a[3]=="2" and a[4]=="45" and a[5]=="7" and a[6]=="5"),"hint":"Revise chage -m/-M/-W/-I."},
 {"label":"aginguser1 deve trocar senha no próximo login","pass":bool(a and a[2]=="0"),"hint":"Force a troca no próximo login."},
 {"label":"aginguser2 possui senha e máximo de 90 dias","pass":password_ok(b) and bool(b and b[4]=="90"),"hint":"Defina senha e chage -M 90."},
 {"label":"aginguser2 expira em 90 dias","pass":bool(b and b[7] and abs(int(b[7])-epoch_days_plus(90))<=1),"hint":"Calcule a data com date e configure chage -E."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj02-05","checks":checks,"score":score},ensure_ascii=False))
"""
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.parse_args()
    p=json_from_remote_python("servera",REMOTE_CHECKER);print(json.dumps(p,ensure_ascii=False));return 0 if p["score"]==100 else 1
if __name__=="__main__":raise SystemExit(main())
