#!/usr/bin/env python3
import argparse, json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import subprocess, json

root = Path("/home/student/rhcsa-lab/obj10-05")
out = root / "output"

def run(args):
    p = subprocess.run(
        args,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return p.returncode, p.stdout.strip()

def read(name):
    p = out / name
    return p.read_text(errors="replace").strip() if p.is_file() else ""

_, mode = run(["getenforce"])
_, ctx = run(["ls", "-Zd", "/srv/avc10"])
_, filectx = run(["ls", "-Z", "/srv/avc10/index.html"])
_, local = run(["sudo", "-n", "semanage", "fcontext", "-l", "-C"])
curl_rc, curl = run(["curl", "-sS", "http://127.0.0.1/avc10/index.html"])

avc = read("avc.txt")
input_avc = root / "input" / "avc.audit"
avc_evidence = (
    bool(avc)
    and ("type=AVC" in avc or "avc:" in avc.lower())
    and "/srv/avc10/index.html" in avc
    and ("httpd" in avc or "httpd_t" in avc)
)

checks = [
    {
        "label": "SELinux permanece enforcing",
        "pass": mode == "Enforcing",
        "hint": "Não use permissive para contornar a negação.",
    },
    {
        "label": "amostra real de AVC está disponível",
        "pass": input_avc.is_file() and input_avc.stat().st_size > 0,
        "hint": "O setup deve fornecer input/avc.audit.",
    },
    {
        "label": "investigação AVC foi registrada",
        "pass": avc_evidence,
        "hint": "Analise input/avc.audit com ausearch -if ... -m AVC.",
    },
    {
        "label": "regra persistente para /srv/avc10 existe",
        "pass": (
            "/srv/avc10" in local
            and "httpd_sys_content_t"
            in "\n".join(x for x in local.splitlines() if "/srv/avc10" in x)
        ),
        "hint": "Use semanage fcontext.",
    },
    {
        "label": "conteúdo está rotulado para httpd",
        "pass": (
            "httpd_sys_content_t" in ctx
            and "httpd_sys_content_t" in filectx
        ),
        "hint": "Use restorecon.",
    },
    {
        "label": "Apache consegue servir o conteúdo",
        "pass": curl_rc == 0 and curl.strip() == "OBJ10 AVC recovered",
        "hint": "Valide com curl local.",
    },
    {
        "label": "evidências finais foram salvas",
        "pass": (
            "httpd_sys_content_t" in read("context.txt")
            and "OBJ10 AVC recovered" in read("curl.txt")
        ),
        "hint": "Salve context.txt e curl.txt.",
    },
]

score = round(sum(c["pass"] for c in checks) / len(checks) * 100)
print(json.dumps(
    {"lab_id": "obj10-05", "checks": checks, "score": score},
    ensure_ascii=False,
))
"""

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--json", action="store_true")
    p.parse_args()
    result = json_from_remote_python("servera", REMOTE_CHECKER)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["score"] == 100 else 1

if __name__ == "__main__":
    raise SystemExit(main())
