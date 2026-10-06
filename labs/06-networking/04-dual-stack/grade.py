#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json
import subprocess

def run(args):
    p = subprocess.run(
        args,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return p.returncode, p.stdout.strip()

def g(field):
    # nmcli -g uses terse output; disable escaping so IPv6 addresses retain ':'.
    return run([
        "nmcli", "--escape", "no", "-g", field,
        "con", "show", "ex200-dual"
    ])[1]

_, a4 = run(["ip", "-4", "-o", "addr", "show", "dev", "ex200a"])
_, a6 = run(["ip", "-6", "-o", "addr", "show", "dev", "ex200a"])

root = Path("/home/student/rhcsa-lab/obj06-04/output")
p4, _ = run(["ping", "-c", "1", "-W", "1", "10.66.4.254"])
p6, _ = run(["ping", "-6", "-c", "1", "-W", "1", "fd00:66:4::fe"])

checks = [
    {
        "label": "IPv4 manual correto",
        "pass": (
            g("ipv4.method") == "manual"
            and "10.66.4.10/24" in g("ipv4.addresses")
        ),
        "hint": "Configure IPv4 manual.",
    },
    {
        "label": "IPv6 manual correto",
        "pass": (
            g("ipv6.method") == "manual"
            and "fd00:66:4::10/64" in g("ipv6.addresses").lower()
        ),
        "hint": "Configure IPv6 manual.",
    },
    {
        "label": "dual-stack aplicado no runtime",
        "pass": (
            "10.66.4.10/24" in a4
            and "fd00:66:4::10/64" in a6.lower()
        ),
        "hint": "Ative o perfil.",
    },
    {
        "label": "autoconnect habilitado",
        "pass": g("connection.autoconnect") == "yes",
        "hint": "Configure autoconnect yes.",
    },
    {
        "label": "conectividade v4/v6 comprovada",
        "pass": (
            p4 == 0
            and p6 == 0
            and (root / "ping4.txt").is_file()
            and (root / "ping6.txt").is_file()
        ),
        "hint": "Teste os dois protocolos.",
    },
]

score = round(sum(c["pass"] for c in checks) / len(checks) * 100)
print(json.dumps(
    {"lab_id": "obj06-04", "checks": checks, "score": score},
    ensure_ascii=False,
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
