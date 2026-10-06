#!/usr/bin/env python3
import argparse, json
from labctl.remote import json_from_remote_python
REMOTE_CHECKER = r"""
from pathlib import Path
import json,subprocess
def run(a):
 p=subprocess.run(a,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE); return p.returncode,p.stdout.strip()
_,cur=run(['hostname']); _,static=run(['hostnamectl','--static']); hosts=Path('/etc/hosts').read_text(errors='replace')
r=Path('/home/student/rhcsa-lab/obj06-06/output'); t=lambda n:(r/n).read_text(errors='replace') if (r/n).is_file() else ''
pingrc,_=run(['ping','-c','1','-W','1','peer06'])
checks=[
 {'label':'hostname temporário foi registrado','pass':t('temporary-hostname.txt').strip()=='temporary-net','hint':'Use hostname temporary-net antes do hostname persistente.'},
 {'label':'hostname persistente correto','pass':cur=='nodea.lab.test' and static=='nodea.lab.test','hint':'Use hostnamectl set-hostname.'},
 {'label':'alias local está no hosts','pass':'10.66.6.254' in hosts and 'peer06' in hosts,'hint':'Adicione a entrada solicitada.'},
 {'label':'getent usa resolução local','pass':'10.66.6.254' in t('getent.txt'),'hint':'Use getent hosts peer06.'},
 {'label':'alias responde','pass':pingrc==0 and (r/'ping.txt').is_file(),'hint':'Teste ping peer06.'},]
score=round(sum(c['pass'] for c in checks)/len(checks)*100); print(json.dumps({'lab_id':'obj06-06','checks':checks,'score':score},ensure_ascii=False))
"""
def main():
    p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
    result=json_from_remote_python("servera",REMOTE_CHECKER)
    print(json.dumps(result,ensure_ascii=False))
    return 0 if result["score"]==100 else 1
if __name__ == "__main__": raise SystemExit(main())
