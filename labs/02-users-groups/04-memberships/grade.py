#!/usr/bin/env python3
import argparse,json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER=r"""
import json,pwd,grp,subprocess

u1=pwd.getpwnam("teamuser1")
u2=pwd.getpwnam("teamuser2")

def groups(user):
    return (
        {g.gr_name for g in grp.getgrall() if user in g.gr_mem}
        | {grp.getgrgid(pwd.getpwnam(user).pw_gid).gr_name}
    )

def sudo_file_owner_group(path):
    # The student's home is normally mode 0700.  The grader runs as
    # student, so direct pathlib.stat() of another user's home can raise
    # PermissionError.  Inspect the final state through the lab's
    # passwordless sudo channel instead.
    is_file = subprocess.run(
        ["sudo", "-n", "test", "-f", path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0

    stat_proc = subprocess.run(
        ["sudo", "-n", "stat", "-c", "%U:%G", path],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    return is_file, stat_proc.stdout.strip() if stat_proc.returncode == 0 else ""

file_ok, owner_group = sudo_file_owner_group(
    "/home/teamuser1/projecta-owned.txt"
)

checks=[
 {"label":"teamuser1 mantém grupo primário privado","pass":grp.getgrgid(u1.pw_gid).gr_name=="teamuser1","hint":"Não altere o grupo primário padrão de teamuser1."},
 {"label":"teamuser1 pertence a projecta","pass":"projecta" in groups("teamuser1"),"hint":"Adicione projecta como grupo suplementar."},
 {"label":"teamuser2 usa projectb como grupo primário","pass":grp.getgrgid(u2.pw_gid).gr_name=="projectb","hint":"Use usermod -g."},
 {"label":"teamuser2 também pertence a projecta","pass":"projecta" in groups("teamuser2"),"hint":"Preserve/addicione a associação suplementar."},
 {"label":"arquivo criado pela troca temporária pertence a projecta","pass":file_ok and owner_group=="teamuser1:projecta","hint":"Use newgrp projecta antes de criar o arquivo."},
]

score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj02-04","checks":checks,"score":score},ensure_ascii=False))
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.parse_args()
    p=json_from_remote_python("servera",REMOTE_CHECKER)
    print(json.dumps(p,ensure_ascii=False))
    return 0 if p["score"]==100 else 1

if __name__=="__main__":
    raise SystemExit(main())
