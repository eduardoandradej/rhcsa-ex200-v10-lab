#!/usr/bin/env python3
import argparse
import json
from labctl.remote import json_from_remote_python

REMOTE_CHECKER = r"""
from pathlib import Path
import json, subprocess

root=Path("/home/student/rhcsa-lab/obj03-02")
rpmfile=root/"rhcsa-inspect-1.0-1.noarch.rpm"
def text(rel):
    p=root/rel
    return p.read_text(errors="replace") if p.is_file() else ""

installed=subprocess.run(["rpm","-q","rhcsa-inspect"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0
checks=[
 {"label":"informações do RPM foram consultadas","pass":"Name" in text("output/info.txt") and "rhcsa-inspect" in text("output/info.txt") and "1.0" in text("output/info.txt"),"hint":"Use rpm -qpi no arquivo."},
 {"label":"lista de arquivos do RPM foi consultada","pass":"/usr/local/bin/rhcsa-inspect" in text("output/files.txt") and "/etc/rhcsa-inspect.conf" in text("output/files.txt"),"hint":"Use rpm -qpl."},
 {"label":"arquivo de configuração foi identificado","pass":"/etc/rhcsa-inspect.conf" in text("output/configs.txt"),"hint":"Use rpm -qpc."},
 {"label":"scriptlets foram inspecionados","pass":"rhcsa-inspect installed" in text("output/scripts.txt"),"hint":"Use rpm -qp --scripts."},
 {"label":"conteúdo foi extraído com sucesso","pass":(root/"extracted/etc/rhcsa-inspect.conf").is_file() and (root/"extracted/usr/local/bin/rhcsa-inspect").is_file(),"hint":"Use rpm2cpio ... | cpio -id."},
 {"label":"pacote permaneceu não instalado","pass":not installed,"hint":"Este laboratório é somente de inspeção."},
]
score=round(sum(c["pass"] for c in checks)/len(checks)*100)
print(json.dumps({"lab_id":"obj03-02","checks":checks,"score":score},ensure_ascii=False))
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
