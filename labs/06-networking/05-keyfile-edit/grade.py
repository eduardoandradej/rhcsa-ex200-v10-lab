#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json
import subprocess

KEYFILE = "/etc/NetworkManager/system-connections/ex200-keyfile.nmconnection"
ROOT = Path("/home/student/rhcsa-lab/obj06-05/output")

def run(args):
    p = subprocess.run(
        args,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return p.returncode, p.stdout.strip()

def nm(field):
    return run([
        "nmcli", "--escape", "no", "-g", field,
        "con", "show", "ex200-keyfile"
    ])[1]

def privileged_read(path):
    rc, out = run(["sudo", "-n", "cat", path])
    return out if rc == 0 else ""

_, runtime = run(["ip", "-4", "-o", "addr", "show", "dev", "ex200a"])
keyfile_text = privileged_read(KEYFILE)

def text(name):
    p = ROOT / name
    return p.read_text(errors="replace") if p.is_file() else ""

checks = [
    {
        "label": "keyfile contém o segundo endereço",
        "pass": (
            "10.66.5.10/24" in keyfile_text
            and "10.66.5.110/24" in keyfile_text
        ),
        "hint": "Edite diretamente o arquivo .nmconnection.",
    },
    {
        "label": "configuração persistente contém os dois IPv4",
        "pass": (
            "10.66.5.10/24" in nm("ipv4.addresses")
            and "10.66.5.110/24" in nm("ipv4.addresses")
        ),
        "hint": "Após editar, use nmcli con reload.",
    },
    {
        "label": "runtime contém os dois IPv4",
        "pass": (
            "10.66.5.10/24" in runtime
            and "10.66.5.110/24" in runtime
        ),
        "hint": "Reative ex200-keyfile depois do reload.",
    },
    {
        "label": "evidência de runtime foi salva",
        "pass": (
            "10.66.5.10/24" in text("runtime.txt")
            and "10.66.5.110/24" in text("runtime.txt")
        ),
        "hint": "Salve ip -4 -br addr show ex200a em output/runtime.txt.",
    },
]

score = round(sum(c["pass"] for c in checks) / len(checks) * 100)
print(json.dumps(
    {"lab_id": "obj06-05", "checks": checks, "score": score},
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
