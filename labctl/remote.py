from __future__ import annotations

import json
import subprocess

from .common import ansible_dir


def _run(
    args: list[str],
    *,
    input_text: str | None = None,
    timeout: int = 30,
) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        cwd=str(ansible_dir()),
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=timeout,
    )


def inventory_host(name: str) -> dict:
    proc = _run(["ansible-inventory", "--host", name])
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "ansible-inventory failed")
    return json.loads(proc.stdout)


def ssh_command(name: str) -> tuple[list[str], str]:
    data = inventory_host(name)
    user = str(data.get("ansible_user", "student"))
    key = data.get("ansible_ssh_private_key_file")

    args = [
        "ssh",
        "-o", "BatchMode=yes",
        "-o", "ConnectTimeout=8",
    ]
    if key:
        args += ["-i", str(key)]

    return args, f"{user}@{name}"


def run_remote_python(
    host: str,
    source: str,
    *,
    timeout: int = 30,
) -> subprocess.CompletedProcess:
    ssh_args, target = ssh_command(host)
    return _run(
        ssh_args + [target, "python3", "-"],
        input_text=source,
        timeout=timeout,
    )


def json_from_remote_python(
    host: str,
    source: str,
    *,
    timeout: int = 30,
) -> dict:
    proc = run_remote_python(host, source, timeout=timeout)

    if proc.returncode != 0:
        raise RuntimeError(
            proc.stderr.strip()
            or proc.stdout.strip()
            or f"remote checker failed on {host}"
        )

    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"remote checker on {host} returned invalid JSON"
        ) from exc
