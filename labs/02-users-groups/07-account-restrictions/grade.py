#!/usr/bin/env python3
import argparse,json
from labctl.remote import json_from_remote_python
REMOTE_CHECKER=r"""
import json,subprocess,pwd
def sh(name):
    p=subprocess.run(["sudo","-n","getent","shadow",name],text=True,stdout=subprocess.PIPE)
    return p.stdout.rstrip("\n").split(":") if p.returncode==0 else None
def exp(days):
    p=subprocess.run(["date","-d",f"+{days} days","+%s"],text=True,stdout=subprocess.PIPE)
    return int(p.stdout.strip())//86400
d=sh("departed1"); t=sh("tempcontract"); r=sh("recoveruser")
checks=[
 {"label":"departed1 está bloqueado e expirado","pass":bool(d and d[1].startswith("!") and d[7]=="1"),"hint":"Use usermod -L -e 1."},
 {"label":"serviceacct usa /sbin/nologin","pass":pwd.getpwnam("serviceacct").pw_shell=="/sbin/nologin","hint":"Altere o login shell."},
 {"label":"tempcontract expira em 30 dias","pass":bool(t and t[7] and abs(int(t[7])-exp(30))<=1),"hint":"Use date e usermod/chage para definir expiração."},
 {"label":"recoveruser foi desbloqueado e não possui expiração","pass":bool(r and not r[1].startswith("!") and r[7]==""),"hint":"Use usermod -U e remova a data de expiração."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj02-07","checks":checks,"score":score},ensure_ascii=False))
"""
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.parse_args()
    p=json_from_remote_python("servera",REMOTE_CHECKER);print(json.dumps(p,ensure_ascii=False));return 0 if p["score"]==100 else 1
if __name__=="__main__":raise SystemExit(main())
