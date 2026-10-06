#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json, subprocess

def run(args):
    p = subprocess.run(
        args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return p.returncode, p.stdout.strip()

def g(field):
    return run(["nmcli", "-g", field, "con", "show", "ex200-mod"])[1]

_, ips = run(["ip", "-4", "-o", "addr", "show", "dev", "ex200a"])
_, defs = run(["ip", "-4", "route", "show", "default", "dev", "ex200a"])

root = Path("/home/student/rhcsa-lab/obj06-03/output")

def t(name):
    p = root / name
    return p.read_text(errors="replace") if p.is_file() else ""

ping_rc, _ = run(["ping", "-c", "1", "-W", "1", "10.66.3.254"])
gateway = g("ipv4.gateway")

checks = [
    {
        "label": "primary alterado",
        "pass": "10.66.3.20/24" in g("ipv4.addresses"),
        "hint": "Substitua o endereço IPv4 primário.",
    },
    {
        "label": "secondary adicionado",
        "pass": "10.66.3.120/24" in g("ipv4.addresses"),
        "hint": "Adicione o endereço secundário.",
    },
    {
        "label": "never-default ativo e gateway ausente",
        "pass": (
            g("ipv4.never-default") == "yes"
            and gateway in ("", "--")
            and not defs
        ),
        "hint": "Use never-default yes e mantenha ipv4.gateway vazio.",
    },
    {
        "label": "runtime tem os dois endereços",
        "pass": (
            "10.66.3.20/24" in ips
            and "10.66.3.120/24" in ips
        ),
        "hint": "Reative o perfil após modificar os endereços.",
    },
    {
        "label": "autoconnect/evidências/conectividade",
        "pass": (
            g("connection.autoconnect") == "yes"
            and "10.66.3.20/24" in t("profile.txt")
            and "10.66.3.120/24" in t("runtime.txt")
            and t("ping.txt")
            and ping_rc == 0
        ),
        "hint": "Salve as evidências e teste o peer diretamente conectado.",
    },
]

score = round(sum(c["pass"] for c in checks) / len(checks) * 100)
print(json.dumps(
    {"lab_id": "obj06-03", "checks": checks, "score": score},
    ensure_ascii=False
))
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.parse_args()

    result = json_from_remote_python("servera", REMOTE_CHECKER)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["score"] == 100 else 1

if __name__ == "__main__":
    raise SystemExit(main())
