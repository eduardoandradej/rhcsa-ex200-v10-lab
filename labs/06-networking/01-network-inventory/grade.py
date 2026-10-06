#!/usr/bin/env python3
import argparse, json
from labctl.remote import json_from_remote_python
REMOTE_CHECKER = r"""
from pathlib import Path
import json
r=Path('/home/student/rhcsa-lab/obj06-01/output')
def t(n):
 p=r/n; return p.read_text(errors='replace') if p.is_file() else ''
checks=[
 {'label':'devices contém ex200a/ex200b','pass':'ex200a' in t('devices.txt') and 'ex200b' in t('devices.txt'),'hint':'Use nmcli device status.'},
 {'label':'connections contém ex200-peer','pass':'ex200-peer' in t('connections.txt'),'hint':'Use nmcli connection show.'},
 {'label':'active contém ex200-peer','pass':'ex200-peer' in t('active.txt'),'hint':'Use nmcli connection show --active.'},
 {'label':'link de ex200a foi salvo','pass':'ex200a' in t('ex200a-link.txt'),'hint':'Use ip -br link show ex200a.'},]
score=round(sum(c['pass'] for c in checks)/len(checks)*100)
print(json.dumps({'lab_id':'obj06-01','checks':checks,'score':score},ensure_ascii=False))
"""
def main():
    p=argparse.ArgumentParser(); p.add_argument("--json",action="store_true"); p.parse_args()
    result=json_from_remote_python("servera",REMOTE_CHECKER)
    print(json.dumps(result,ensure_ascii=False))
    return 0 if result["score"]==100 else 1
if __name__ == "__main__": raise SystemExit(main())
