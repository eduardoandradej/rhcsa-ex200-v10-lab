#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from labctl.remote import json_from_remote_python


REMOTE_CHECKER = r"""
from pathlib import Path
import json
import tarfile

root = Path("/home/student/rhcsa-lab/obj01-05")
out = root / "output"

expected = {
    "project/config/app.conf": "service=rhcsa-lab\nworkers=4\n",
    "project/docs/readme.txt": "RHCSA archive practice\n",
    "project/inventory.txt": "servera\nserverb\n",
}

def archive_ok(path, mode):
    if not path.is_file():
        return False
    try:
        with tarfile.open(path, mode) as tf:
            names = set(tf.getnames())
            return set(expected).issubset(names)
    except (tarfile.TarError, OSError):
        return False

def restored_ok(directory):
    return all(
        (directory / rel).is_file()
        and (directory / rel).read_text() == content
        for rel, content in expected.items()
    )

checks = [
    {
        "label": "archive TAR foi criado",
        "pass": archive_ok(out / "project.tar", "r:"),
        "hint": "project.tar deve conter a árvore project.",
    },
    {
        "label": "archive gzip é válido",
        "pass": archive_ok(out / "project.tar.gz", "r:gz"),
        "hint": "Crie um archive gzip válido preservando project.tar.",
    },
    {
        "label": "archive bzip2 é válido",
        "pass": archive_ok(out / "project.tar.bz2", "r:bz2"),
        "hint": "Crie um archive bzip2 válido preservando project.tar.",
    },
    {
        "label": "conteúdo gzip foi restaurado corretamente",
        "pass": restored_ok(root / "restore-gzip"),
        "hint": "Extraia project.tar.gz em restore-gzip.",
    },
    {
        "label": "conteúdo bzip2 foi restaurado corretamente",
        "pass": restored_ok(root / "restore-bzip2"),
        "hint": "Extraia project.tar.bz2 em restore-bzip2.",
    },
]

score = round(sum(1 for c in checks if c["pass"]) / len(checks) * 100)
print(json.dumps({"lab_id": "obj01-05", "checks": checks, "score": score}, ensure_ascii=False))
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.parse_args()

    payload = json_from_remote_python("servera", REMOTE_CHECKER)
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if payload.get("score") == 100 else 1


if __name__ == "__main__":
    raise SystemExit(main())
