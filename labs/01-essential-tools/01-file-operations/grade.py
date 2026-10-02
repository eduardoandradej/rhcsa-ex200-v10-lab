#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from labctl.remote import json_from_remote_python


REMOTE_CHECKER = r"""
from pathlib import Path
import json

root = Path("/home/student/rhcsa-lab/obj01-01")
input_dir = root / "input"
workspace = root / "workspace"

expected_reports = {
    "report-alpha.txt": "alpha: systems inventory\n",
    "report-beta.txt": "beta: storage inventory\n",
    "report-gamma.txt": "gamma: network inventory\n",
}
expected_images = {
    "image-01.jpg": "training-image-01\n",
    "image-02.jpg": "training-image-02\n",
}
expected_notes = "review file operations before the next lab\n"

def exact_files(directory, expected):
    return all(
        (directory / name).is_file()
        and (directory / name).read_text() == content
        for name, content in expected.items()
    )

checks = []

workspace_dirs = all(
    (workspace / name).is_dir()
    for name in ("reports", "images", "notes")
)
checks.append({
    "label": "workspace e subdiretórios existem",
    "pass": workspace_dirs,
    "hint": "Verifique workspace/reports, workspace/images e workspace/notes.",
})

reports_ok = (
    exact_files(input_dir, expected_reports)
    and exact_files(workspace / "reports", expected_reports)
)
checks.append({
    "label": "reports foram copiados e as origens preservadas",
    "pass": reports_ok,
    "hint": "Os report-*.txt devem existir tanto em input quanto em workspace/reports.",
})

images_ok = (
    exact_files(workspace / "images", expected_images)
    and all(not (input_dir / name).exists() for name in expected_images)
)
checks.append({
    "label": "images foram movidas para workspace/images",
    "pass": images_ok,
    "hint": "As image-*.jpg não devem permanecer em input.",
})

notes_ok = (
    (workspace / "notes" / "notes-final.txt").is_file()
    and (workspace / "notes" / "notes-final.txt").read_text() == expected_notes
    and not (input_dir / "notes-old.txt").exists()
)
checks.append({
    "label": "notes-old.txt foi movido e renomeado",
    "pass": notes_ok,
    "hint": "O destino esperado é workspace/notes/notes-final.txt.",
})

empty_notes = all(
    (workspace / "notes" / f"note-{n}.txt").is_file()
    and (workspace / "notes" / f"note-{n}.txt").stat().st_size == 0
    for n in range(1, 4)
)
checks.append({
    "label": "note-1.txt, note-2.txt e note-3.txt existem e estão vazios",
    "pass": empty_notes,
    "hint": "Crie exatamente os três arquivos vazios em workspace/notes.",
})

tmp_removed = not any(input_dir.glob("*.tmp"))
checks.append({
    "label": "arquivos .tmp foram removidos de input",
    "pass": tmp_removed,
    "hint": "Não deve restar nenhum arquivo *.tmp em input.",
})

passed = sum(1 for item in checks if item["pass"])
score = round((passed / len(checks)) * 100)

print(json.dumps({
    "lab_id": "obj01-01",
    "checks": checks,
    "score": score,
}, ensure_ascii=False))
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
