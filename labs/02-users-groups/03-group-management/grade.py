#!/usr/bin/env python3
import argparse,json
from labctl.remote import json_from_remote_python
REMOTE_CHECKER=r"""
import grp,json
def g(name):
    try:return grp.getgrnam(name)
    except KeyError:return None
linux=g("linuxops"); audit=g("auditteam"); dev=g("devopsgrp")
checks=[
 {"label":"linuxops possui GID 33010","pass":bool(linux and linux.gr_gid==33010),"hint":"Revise groupadd -g."},
 {"label":"auditteam existe","pass":audit is not None,"hint":"Crie auditteam."},
 {"label":"devtemp foi renomeado para devopsgrp","pass":g("devtemp") is None and dev is not None,"hint":"Use groupmod -n."},
 {"label":"devopsgrp possui GID 33022","pass":bool(dev and dev.gr_gid==33022),"hint":"Use groupmod -g."},
 {"label":"oldgrp foi removido","pass":g("oldgrp") is None,"hint":"Use groupdel."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj02-03","checks":checks,"score":score},ensure_ascii=False))
"""
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.parse_args()
    p=json_from_remote_python("servera",REMOTE_CHECKER);print(json.dumps(p,ensure_ascii=False));return 0 if p["score"]==100 else 1
if __name__=="__main__":raise SystemExit(main())
