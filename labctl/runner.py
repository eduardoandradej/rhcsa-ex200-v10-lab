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

    # A valid grader is allowed to return 0 (PASS) or 1 (INCOMPLETE),
    # but in both cases it must emit a JSON payload.
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        detail = (
            proc.stderr.strip()
            or proc.stdout.strip()
            or f"grader terminou com rc={proc.returncode} sem saída JSON"
        )
        raise RuntimeError(
            "grader falhou antes de retornar JSON:\n" + detail
        ) from exc

    if proc.returncode not in (0, 1):
        detail = proc.stderr.strip() or f"grader terminou com rc={proc.returncode}"
        raise RuntimeError(detail)

    return proc.returncode, payload
