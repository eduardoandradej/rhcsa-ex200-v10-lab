#!/usr/bin/env python3
import argparse, json, re
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import os, pwd, grp, stat, subprocess, json, re

root = Path("/home/student/rhcsa-lab/obj12-01/output")

def run(args):
    p = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.returncode, p.stdout.strip()

def read(name):
    p = root / name
    return p.read_text(errors="replace").strip() if p.is_file() else ""

try:
    pw = pwd.getpwnam("analyst12")
    user_ok = pw.pw_shell == "/bin/bash"
    groups = [g.gr_name for g in grp.getgrall() if "analyst12" in g.gr_mem]
except KeyError:
    user_ok = False
    groups = []

try:
    gr = grp.getgrnam("ops12")
    group_gid = gr.gr_gid
except KeyError:
    group_gid = -1

d = Path("/srv/team12")
dir_ok = False
if d.is_dir():
    st = d.stat()
    dir_ok = (
        st.st_uid == 0
        and st.st_gid == group_gid
        and stat.S_IMODE(st.st_mode) == 0o2770
    )

_, shadow = run(["sudo", "-n", "chage", "-l", "analyst12"])
aging = (
    ("Minimum number of days between password change" in shadow and ": 2" in shadow)
    and ("Maximum number of days between password change" in shadow and ": 45" in shadow)
    and ("Number of days of warning before password expires" in shadow and ": 7" in shadow)
)

_, acl = run(["getfacl", "-cp", "/srv/team12"])
acl_ok = bool(re.search(r"(?m)^user:student:rwx$", acl))

files_ok = all((d / x).is_file() for x in ("alpha.txt", "beta.txt"))
script = Path("/usr/local/bin/count-team12")
script_ok = script.is_file() and os.access(script, os.X_OK)
count_rc, count = run(["/usr/local/bin/count-team12", "/srv/team12"]) if script_ok else (1, "")

checks = [
    {"label":"usuário e grupo foram configurados", "pass":user_ok and "ops12" in groups, "hint":"Crie analyst12 com shell bash e grupo suplementar ops12."},
    {"label":"política de aging está correta", "pass":aging, "hint":"Configure min=2, max=45 e warn=7."},
    {"label":"diretório compartilhado usa root:ops12 e 2770", "pass":dir_ok, "hint":"Aplique grupo e setgid em /srv/team12."},
    {"label":"ACL concede rwx ao student", "pass":acl_ok, "hint":"Use setfacl para o usuário student."},
    {"label":"arquivos e script estão funcionais", "pass":files_ok and script_ok and count_rc == 0 and count == "2", "hint":"O script deve contar apenas arquivos regulares diretos."},
    {"label":"evidências finais foram salvas", "pass":"analyst12" in read("id.txt") and "ops12" in read("id.txt") and "student:rwx" in read("acl.txt") and read("count.txt") == "2", "hint":"Salve id, chage, ACL e count."},
]
score = round(sum(c["pass"] for c in checks) / len(checks) * 100)
print(json.dumps({"lab_id":"obj12-01","checks":checks,"score":score}, ensure_ascii=False))
"""

def main():
    p=argparse.ArgumentParser(); p.add_argument("--json", action="store_true"); p.parse_args()
    r=json_from_remote_python("servera", REMOTE_CHECKER)
    print(json.dumps(r, ensure_ascii=False))
    return 0 if r["score"] == 100 else 1

if __name__ == "__main__":
    raise SystemExit(main())
