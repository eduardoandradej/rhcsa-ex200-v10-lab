#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
import grp
import json
import subprocess
from pathlib import Path

def shadow(name):
    p = subprocess.run(
        ["sudo", "-n", "getent", "shadow", name],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return p.stdout.rstrip("\n").split(":") if p.returncode == 0 else None

def exp(days):
    p = subprocess.run(
        ["date", "-d", f"+{days} days", "+%s"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return int(p.stdout.strip()) // 86400

def login_defs_max():
    value = None
    for line in Path("/etc/login.defs").read_text().splitlines():
        s = line.strip()
        if s and not s.startswith("#"):
            parts = s.split()
            if parts and parts[0] == "PASS_MAX_DAYS" and len(parts) > 1:
                value = parts[1]
    return value

def cmd(args):
    p = subprocess.run(
        args,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return p.returncode, p.stdout, p.stderr

try:
    group = grp.getgrnam("consultantsx")
except KeyError:
    group = None

sudoers = "/etc/sudoers.d/consultantsx"

rc_file, _, _ = cmd(["sudo", "-n", "test", "-f", sudoers])
rc_mode, mode_out, _ = cmd(["sudo", "-n", "stat", "-c", "%a", sudoers])
rc_visudo, _, _ = cmd(["sudo", "-n", "visudo", "-cf", sudoers])

users = ["consultx1", "consultx2", "consultx3"]
shadow_data = {u: shadow(u) for u in users}
members = set(group.gr_mem) if group else set()
expected_exp = exp(90)

checks = [
    {
        "label": "PASS_MAX_DAYS foi definido como 30",
        "pass": login_defs_max() == "30",
        "hint": "Revise /etc/login.defs.",
    },
    {
        "label": "consultantsx possui GID 35050",
        "pass": bool(group and group.gr_gid == 35050),
        "hint": "Revise groupadd -g.",
    },
    {
        "label": "sudoers.d de consultantsx é válido e modo 0440",
        "pass": (
            rc_file == 0
            and rc_mode == 0
            and mode_out.strip() == "440"
            and rc_visudo == 0
        ),
        "hint": "Revise conteúdo, modo e visudo.",
    },
    {
        "label": "três usuários pertencem a consultantsx",
        "pass": all(u in members for u in users),
        "hint": "Adicione o grupo como suplementar.",
    },
    {
        "label": "três usuários possuem senha definida",
        "pass": all(
            shadow_data[u]
            and shadow_data[u][1]
            and not shadow_data[u][1].startswith(("!", "*"))
            for u in users
        ),
        "hint": "Defina as senhas antes de forçar a troca.",
    },
    {
        "label": "três contas expiram em 90 dias",
        "pass": all(
            shadow_data[u]
            and shadow_data[u][7]
            and abs(int(shadow_data[u][7]) - expected_exp) <= 1
            for u in users
        ),
        "hint": "Use date e chage/usermod.",
    },
    {
        "label": "consultx2 possui máximo de 15 dias",
        "pass": bool(
            shadow_data["consultx2"]
            and shadow_data["consultx2"][4] == "15"
        ),
        "hint": "Aplique política específica em consultx2.",
    },
    {
        "label": "três usuários devem trocar senha no próximo login",
        "pass": all(
            shadow_data[u] and shadow_data[u][2] == "0"
            for u in users
        ),
        "hint": "Force last password change para 0.",
    },
]

score = round(sum(1 for c in checks if c["pass"]) / len(checks) * 100)
print(json.dumps(
    {"lab_id": "obj02-08", "checks": checks, "score": score},
    ensure_ascii=False,
))
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.parse_args()

    payload = json_from_remote_python("serverb", REMOTE_CHECKER)
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload["score"] == 100 else 1

if __name__ == "__main__":
    raise SystemExit(main())
