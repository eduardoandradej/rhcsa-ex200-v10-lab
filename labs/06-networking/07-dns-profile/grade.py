#!/usr/bin/env python3
import argparse, json
from labctl.remote import json_from_remote_python
REMOTE_CHECKER = r"""
from pathlib import Path
import json,subprocess
def run(a):
 p=subprocess.run(a,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE); return p.returncode,p.stdout.strip()
def g(f): return run(['nmcli','-g',f,'con','show','ex200-dns'])[1]
_,act=run(['nmcli','-g','GENERAL.CONNECTION','dev','show','ex200a']); r=Path('/home/student/rhcsa-lab/obj06-07/output'); t=lambda n:(r/n).read_text(errors='replace') if (r/n).is_file() else ''
dns=g('ipv4.dns')
checks=[
 {'label':'dois DNS persistentes','pass':'192.0.2.53' in dns and '192.0.2.54' in dns,'hint':'Configure ipv4.dns.'},
 {'label':'search domain persistente','pass':'lab.example' in g('ipv4.dns-search'),'hint':'Configure ipv4.dns-search.'},
 {'label':'ignore-auto-dns habilitado','pass':g('ipv4.ignore-auto-dns')=='yes','hint':'Configure ignore-auto-dns yes.'},
 {'label':'perfil isolado/inativo','pass':g('ipv4.never-default')=='yes' and g('connection.autoconnect')=='no' and act!='ex200-dns','hint':'Não ative o perfil.'},
 {'label':'evidências salvas','pass':'192.0.2.53' in t('dns-profile.txt') and 'hosts:' in t('nsswitch-hosts.txt'),'hint':'Salve perfil e nsswitch.'},]
score=round(sum(c['pass'] for c in checks)/len(checks)*100); print(json.dumps({'lab_id':'obj06-07','checks':checks,'score':score},ensure_ascii=False))
"""
def main():
    p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
    result=json_from_remote_python("servera",REMOTE_CHECKER)
    print(json.dumps(result,ensure_ascii=False))
    return 0 if result["score"]==100 else 1
if __name__ == "__main__": raise SystemExit(main())
