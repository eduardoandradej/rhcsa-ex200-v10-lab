#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from labctl.remote import json_from_remote_python


REMOTE_CHECKER = r"""
from pathlib import Path
import json
import os

root = Path("/home/student/rhcsa-lab/obj01-07")
source = root / "data/inventory.txt"
hard = root / "links/inventory.hard"
sym_file = root / "links/current.conf"
sym_dir = root / "links/docs"

hard_ok = (
    source.is_file()
    and hard.is_file()
    and source.stat().st_ino == hard.stat().st_ino
    and source.stat().st_nlink >= 2
)

sym_file_ok = (
    sym_file.is_symlink()
    and os.readlink(sym_file) == "../data/app.conf"
    and sym_file.resolve() == (root / "data/app.conf").resolve()
)

sym_dir_ok = (
    sym_dir.is_symlink()
    and os.readlink(sym_dir) == "../data/docs"
    and (sym_dir / "guide.txt").read_text() == "RHCSA links practice\n"
)

checks = [
    {
        "label": "inventory.hard é um hard link real",
        "pass": hard_ok,
        "hint": "O inode deve ser o mesmo de data/inventory.txt.",
    },
    {
        "label": "current.conf é o symbolic link solicitado",
        "pass": sym_file_ok,
        "hint": "O alvo textual esperado é ../data/app.conf.",
    },
    {
        "label": "docs é um symbolic link funcional para o diretório",
        "pass": sym_dir_ok,
        "hint": "O alvo textual esperado é ../data/docs.",
    },
]

score = round(sum(1 for c in checks if c["pass"]) / len(checks) * 100)
print(json.dumps({"lab_id": "obj01-07", "checks": checks, "score": score}, ensure_ascii=False))
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
