from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

from .common import ansible_dir, project_root


def _run(
    args: list[str],
    *,
    cwd: Path | None = None,
    timeout: int = 120,
    env: dict | None = None,
) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
        env=env,
    )


def run_playbook(path: Path) -> subprocess.CompletedProcess:
    return _run(
        ["ansible-playbook", str(path.resolve())],
        cwd=ansible_dir(),
        timeout=180,
    )


def run_grader(path: Path) -> tuple[int, dict]:
    env = os.environ.copy()
    env["RHCSA_LAB_ROOT"] = str(project_root())

    proc = _run(
        ["python3", str(path.resolve()), "--json"],
        cwd=project_root(),
        timeout=60,
        env=env,
    )

    if proc.returncode not in (0, 1):
        raise RuntimeError(
            proc.stderr.strip()
            or proc.stdout.strip()
            or "grader terminou com erro"
        )

    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"grader retornou saída JSON inválida: {exc}"
        ) from exc

    return proc.returncode, payload
