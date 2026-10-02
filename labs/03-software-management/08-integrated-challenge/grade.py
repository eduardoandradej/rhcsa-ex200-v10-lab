#!/usr/bin/env python3
import argparse
import configparser
import json
import subprocess
from pathlib import Path
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import configparser
import json
import subprocess

root = Path("/home/student/rhcsa-lab/obj03-08")
cfg = configparser.ConfigParser()
cfg.read("/etc/yum.repos.d/rhcsa-system.repo")

base = cfg["rhcsa-system-base"] if cfg.has_section("rhcsa-system-base") else {}
err = cfg["rhcsa-system-errata"] if cfg.has_section("rhcsa-system-errata") else {}

def ver(name):
    p = subprocess.run(
        ["rpm", "-q", "--qf", "%{VERSION}-%{RELEASE}\n", name],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return p.returncode, p.stdout.strip()

rc_sys, v_sys = ver("rhcsa-system")
rc_local, v_local = ver("rhcsa-local")

info_path = root / "output/local-rpm-info.txt"
hist_path = root / "output/history.txt"

info = info_path.read_text(errors="replace") if info_path.is_file() else ""
hist = hist_path.read_text(errors="replace") if hist_path.is_file() else ""

history_ok = (
    "rhcsa-system" in hist
    and (
        "Transaction ID" in hist
        or "Transaction ID :" in hist
        or "Command Line" in hist
        or "Command line" in hist
    )
)

checks = [
    {
        "label": "repositório base possui configuração correta",
        "pass": bool(base)
        and base.get("baseurl") == "file:///var/lib/rhcsa-lab/obj03/repos/base"
        and base.get("gpgcheck") == "0",
        "hint": "Revise a seção rhcsa-system-base.",
    },
    {
        "label": "repositório errata possui configuração correta",
        "pass": bool(err)
        and err.get("baseurl") == "file:///var/lib/rhcsa-lab/obj03/repos/errata"
        and err.get("gpgcheck") == "0",
        "hint": "Revise a seção rhcsa-system-errata.",
    },
    {
        "label": "rhcsa-system foi atualizado para 2.0-1",
        "pass": rc_sys == 0 and v_sys == "2.0-1",
        "hint": "Instale v1 pelo base e atualize com errata habilitado.",
    },
    {
        "label": "RPM local rhcsa-local está instalado",
        "pass": rc_local == 0 and v_local == "1.0-1",
        "hint": "Use dnf install no caminho do arquivo RPM.",
    },
    {
        "label": "RPM local foi inspecionado antes da instalação",
        "pass": "rhcsa-local" in info and "1.0" in info,
        "hint": "Use rpm -qpi no arquivo local.",
    },
    {
        "label": "dois repositórios estão desabilitados ao final",
        "pass": bool(base)
        and bool(err)
        and base.get("enabled") == "0"
        and err.get("enabled") == "0",
        "hint": "Desabilite persistentemente base e errata.",
    },
    {
        "label": "detalhes da transação DNF de rhcsa-system foram registrados",
        "pass": history_ok,
        "hint": "Use dnf history list para obter o ID e dnf history info <ID> para salvar os detalhes.",
    },
]

score = round(sum(1 for c in checks if c["pass"]) / len(checks) * 100)
print(json.dumps(
    {"lab_id": "obj03-08", "checks": checks, "score": score},
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
