#!/usr/bin/env python3
import argparse, json
from labctl.remote import json_from_remote_python
REMOTE_CHECKER = r"""
from pathlib import Path
import json,subprocess
def run(a):
 p=subprocess.run(a,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE); return p.returncode,p.stdout.strip()
def g(f): return run(['nmcli','-g',f,'con','show','ex200-static'])[1]
_,act=run(['nmcli','-g','GENERAL.CONNECTION','dev','show','ex200a']); _,ip=run(['ip','-4','-o','addr','show','dev','ex200a'])
p=Path('/home/student/rhcsa-lab/obj06-02/output/ping.txt'); pingrc,_=run(['ping','-c','1','-W','1','10.66.2.254'])
checks=[
 {'label':'perfil associado a ex200a','pass':g('connection.interface-name')=='ex200a','hint':'Use ifname ex200a.'},
 {'label':'IPv4 manual correto','pass':g('ipv4.method')=='manual' and '10.66.2.10/24' in g('ipv4.addresses'),'hint':'Configure endereço/método.'},
 {'label':'IPv6 desabilitado','pass':g('ipv6.method')=='disabled','hint':'Configure ipv6.method disabled.'},
 {'label':'perfil ativo e autoconnect','pass':act=='ex200-static' and g('connection.autoconnect')=='yes','hint':'Ative o perfil e autoconnect.'},
 {'label':'runtime e conectividade corretos','pass':'10.66.2.10/24' in ip and pingrc==0 and p.is_file() and p.stat().st_size>0,'hint':'Ative e teste o peer.'},]
score=round(sum(c['pass'] for c in checks)/len(checks)*100); print(json.dumps({'lab_id':'obj06-02','checks':checks,'score':score},ensure_ascii=False))
"""
def main():
    p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
    result=json_from_remote_python("servera",REMOTE_CHECKER)
    print(json.dumps(result,ensure_ascii=False))
    return 0 if result["score"]==100 else 1
if __name__ == "__main__": raise SystemExit(main())
