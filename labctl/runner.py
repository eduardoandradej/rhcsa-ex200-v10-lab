from __future__ import annotations

import json
import os
from pathlib import Path
import signal
import subprocess

from .common import ansible_dir, project_root


def _run(
    args: list[str],
    *,
    cwd: Path | None = None,
    timeout: int = 120,
    env: dict | None = None,
) -> subprocess.CompletedProcess:
    proc = subprocess.Popen(
        args,
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        start_new_session=True,
    )

    try:
        stdout, stderr = proc.communicate(timeout=timeout)
        return subprocess.CompletedProcess(
            args=args,
            returncode=proc.returncode,
            stdout=stdout or "",
            stderr=stderr or "",
        )
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass

        try:
            stdout, stderr = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            stdout, stderr = proc.communicate()

        message = (
            f"command timed out after {timeout} seconds; "
            "local process group terminated"
        )
        stderr = (stderr or "").rstrip()
        stderr = f"{stderr}\n{message}" if stderr else message

        return subprocess.CompletedProcess(
            args=args,
            returncode=124,
            stdout=stdout or "",
            stderr=stderr,
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
