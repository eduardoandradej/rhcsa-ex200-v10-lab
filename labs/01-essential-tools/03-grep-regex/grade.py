#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from labctl.remote import json_from_remote_python


REMOTE_CHECKER = r"""
from pathlib import Path
import json

root = Path("/home/student/rhcsa-lab/obj01-03")
out = root / "output"

expected = {
    "servers.txt": (
        "SRV-001|web01|prod|active|192.168.100.21\n"
        "SRV-002|web02|prod|active|192.168.100.22\n"
        "SRV-003|db01|prod|maintenance|192.168.100.31\n"
        "SRV-004|api01|prod|active|192.168.100.41\n"
    ),
    "web-hosts.txt": (
        "SRV-001|web01|prod|active|192.168.100.21\n"
        "SRV-002|web02|prod|active|192.168.100.22\n"
        "DEV-101|web-dev01|dev|active|10.10.0.11\n"
        "TST-201|web-test01|test|active|172.16.0.21\n"
    ),
    "prod-active.txt": (
        "SRV-001|web01|prod|active|192.168.100.21\n"
        "SRV-002|web02|prod|active|192.168.100.22\n"
        "SRV-004|api01|prod|active|192.168.100.41\n"
    ),
    "alerts.log": (
        "2026-10-02T10:01:00 WARN web02 response slow\n"
        "2026-10-02T10:03:00 ERROR api01 backend timeout\n"
        "2026-10-02T10:05:00 WARN db01 replication lag\n"
    ),
    "ip-ending-21.txt": (
        "SRV-001|web01|prod|active|192.168.100.21\n"
        "TST-201|web-test01|test|active|172.16.0.21\n"
    ),
}

labels = {
    "servers.txt": "regex selecionou IDs SRV com três dígitos",
    "web-hosts.txt": "regex selecionou hostnames iniciados por web",
    "prod-active.txt": "filtro selecionou sistemas prod e active",
    "alerts.log": "grep -E selecionou WARN ou ERROR",
    "ip-ending-21.txt": "regex selecionou IPs terminados em .21",
}

hints = {
    "servers.txt": "Use âncora de início, classe de dígitos e quantificador.",
    "web-hosts.txt": "Considere os separadores | ao definir o campo hostname.",
    "prod-active.txt": "É possível encadear filtros ou usar uma expressão adequada.",
    "alerts.log": "Use alternância em expressão regular estendida.",
    "ip-ending-21.txt": "Escape o ponto e use âncora de fim.",
}

checks = []
for name, content in expected.items():
    path = out / name
    ok = path.is_file() and path.read_text() == content
    checks.append({
        "label": labels[name],
        "pass": ok,
        "hint": hints[name],
    })

score = round(sum(1 for c in checks if c["pass"]) / len(checks) * 100)
print(json.dumps({"lab_id": "obj01-03", "checks": checks, "score": score}, ensure_ascii=False))
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.parse_args()

    try:
        payload = json_from_remote_python("servera", REMOTE_CHECKER)
    except Exception as exc:
        print(str(exc))
        return 2

    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload.get("score") == 100 else 1


if __name__ == "__main__":
    raise SystemExit(main())
