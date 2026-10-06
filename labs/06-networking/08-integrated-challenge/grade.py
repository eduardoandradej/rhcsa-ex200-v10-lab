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
    # Keep IPv6 values unescaped in terse nmcli output.
    return run([
        "nmcli", "--escape", "no", "-g", field,
        "con", "show", "exam-net"
    ])[1]

_, a4 = run(["ip", "-4", "-o", "addr", "show", "dev", "ex200a"])
_, a6 = run(["ip", "-6", "-o", "addr", "show", "dev", "ex200a"])
_, host = run(["hostnamectl", "--static"])

hosts = Path("/etc/hosts").read_text(errors="replace")
root = Path("/home/student/rhcsa-lab/obj06-08/output")

def t(name):
    p = root / name
    return p.read_text(errors="replace") if p.is_file() else ""

p4, _ = run(["ping", "-c", "1", "-W", "1", "10.66.8.254"])
p6, _ = run(["ping", "-6", "-c", "1", "-W", "1", "fd00:66:8::fe"])

checks = [
    {
        "label": "exam-net associado a ex200a",
        "pass": g("connection.interface-name") == "ex200a",
        "hint": "Use ifname ex200a.",
    },
    {
        "label": "dois IPv4 persistentes",
        "pass": (
            "10.66.8.20/24" in g("ipv4.addresses")
            and "10.66.8.120/24" in g("ipv4.addresses")
        ),
        "hint": "Configure primary+secondary.",
    },
    {
        "label": "IPv6 persistente",
        "pass": (
            g("ipv6.method") == "manual"
            and "fd00:66:8::20/64" in g("ipv6.addresses").lower()
        ),
        "hint": "Configure IPv6 manual.",
    },
    {
        "label": "runtime dual-stack correto",
        "pass": (
            "10.66.8.20/24" in a4
            and "10.66.8.120/24" in a4
            and "fd00:66:8::20/64" in a6.lower()
        ),
        "hint": "Ative o perfil.",
    },
    {
        "label": "hostname e hosts corretos",
        "pass": (
            host == "serverb-net.lab.test"
            and "peer-net" in hosts
            and "10.66.8.254" in t("getent.txt")
        ),
        "hint": "Configure hostname e /etc/hosts.",
    },
    {
        "label": "conectividade IPv4/IPv6",
        "pass": (
            p4 == 0
            and p6 == 0
            and (root / "ping4.txt").is_file()
            and (root / "ping6.txt").is_file()
        ),
        "hint": "Teste os dois protocolos.",
    },
    {
        "label": "evidências de perfil/runtime",
        "pass": (
            "exam-net" in t("profile.txt")
            and "10.66.8.120/24" in t("runtime.txt")
        ),
        "hint": "Salve profile/runtime.",
    },
    {
        "label": "autoconnect habilitado sem gateways",
        "pass": (
            g("connection.autoconnect") == "yes"
            and g("ipv4.gateway") in ("", "--")
            and g("ipv6.gateway") in ("", "--")
        ),
        "hint": "Autoconnect yes, sem gateway.",
    },
]

score = round(sum(c["pass"] for c in checks) / len(checks) * 100)
print(json.dumps(
    {"lab_id": "obj06-08", "checks": checks, "score": score},
    ensure_ascii=False,
))
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.parse_args()

    result = json_from_remote_python("serverb", REMOTE_CHECKER)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["score"] == 100 else 1

if __name__ == "__main__":
    raise SystemExit(main())
