#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
import grp
import json
import subprocess

sudoers = "/etc/sudoers.d/opsadmin"

def cmd(args):
    p = subprocess.run(
        args,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return p.returncode, p.stdout, p.stderr

members = set(grp.getgrnam("opsadmin").gr_mem)

rc_file, _, _ = cmd(["sudo", "-n", "test", "-f", sudoers])
rc_mode, mode_out, _ = cmd(["sudo", "-n", "stat", "-c", "%a", sudoers])
rc_visudo, _, _ = cmd(["sudo", "-n", "visudo", "-cf", sudoers])

rc_id, id_out, _ = cmd([
    "sudo", "-n", "-u", "svcadmin",
    "sudo", "-n", "/usr/bin/id", "-u"
])

rc_whoami, whoami_out, _ = cmd([
    "sudo", "-n", "-u", "svcadmin",
    "sudo", "-n", "/usr/bin/whoami"
])

# A command not listed in the requested policy must not be authorized
# non-interactively.
rc_unlisted, _, _ = cmd([
    "sudo", "-n", "-u", "svcadmin",
    "sudo", "-n", "/usr/bin/hostname"
])

checks = [
    {
        "label": "svcadmin pertence a opsadmin",
        "pass": "svcadmin" in members,
        "hint": "Adicione o usuário ao grupo suplementar.",
    },
    {
        "label": "arquivo sudoers.d existe com modo 0440",
        "pass": rc_file == 0 and rc_mode == 0 and mode_out.strip() == "440",
        "hint": "Revise caminho e permissões.",
    },
    {
        "label": "configuração sudoers é sintaticamente válida",
        "pass": rc_visudo == 0,
        "hint": "Use visudo -cf.",
    },
    {
        "label": "svcadmin executa id como root sem senha",
        "pass": rc_id == 0 and id_out.strip() == "0",
        "hint": "Revise NOPASSWD e a permissão para /usr/bin/id.",
    },
    {
        "label": "svcadmin executa whoami como root sem senha",
        "pass": rc_whoami == 0 and whoami_out.strip() == "root",
        "hint": "Revise a permissão para /usr/bin/whoami.",
    },
    {
        "label": "comando não listado não recebeu sudo sem senha",
        "pass": rc_unlisted != 0,
        "hint": "A política deve limitar o usuário aos comandos solicitados.",
    },
]

score = round(sum(1 for c in checks if c["pass"]) / len(checks) * 100)
print(json.dumps(
    {"lab_id": "obj02-06", "checks": checks, "score": score},
    ensure_ascii=False,
))
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.parse_args()

    payload = json_from_remote_python("servera", REMOTE_CHECKER)
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload["score"] == 100 else 1

if __name__ == "__main__":
    raise SystemExit(main())
