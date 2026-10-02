from __future__ import annotations

from dataclasses import dataclass
import json
import shutil
import subprocess
from pathlib import Path
import socket

from .common import ansible_dir


@dataclass
class NodeStatus:
    name: str
    address: str
    role: str
    online: bool
    detail: str = ""


def _run(args: list[str], cwd: Path | None = None, timeout: int = 20) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )


def _inventory_hosts() -> dict[str, dict]:
    workdir = ansible_dir()
    proc = _run(["ansible-inventory", "--list"], cwd=workdir)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "falha em ansible-inventory")

    data = json.loads(proc.stdout)
    hostvars = data.get("_meta", {}).get("hostvars", {})

    def members(group: str) -> set[str]:
        item = data.get(group, {})
        return set(item.get("hosts", []))

    control = members("control")
    managed = members("managed")

    result: dict[str, dict] = {}
    for name, vars_ in hostvars.items():
        role = "control" if name in control else "managed" if name in managed else "other"
        address = vars_.get("ansible_host")
        if not address:
            try:
                address = socket.gethostbyname(name)
            except OSError:
                address = name

        result[name] = {
            "address": address,
            "role": role,
        }
    return result


def _ping_host(name: str) -> tuple[bool, str]:
    workdir = ansible_dir()
    proc = _run(
        ["ansible", name, "-m", "ansible.builtin.ping", "-o"],
        cwd=workdir,
        timeout=15,
    )

    output = (proc.stdout + "\n" + proc.stderr).strip()
    online = proc.returncode == 0 and "SUCCESS" in proc.stdout and '"ping": "pong"' in proc.stdout
    return online, output


def node_statuses() -> list[NodeStatus]:
    inventory = _inventory_hosts()
    statuses: list[NodeStatus] = []

    for name in sorted(inventory):
        meta = inventory[name]
        online, detail = _ping_host(name)
        statuses.append(
            NodeStatus(
                name=name,
                address=str(meta["address"]),
                role=str(meta["role"]),
                online=online,
                detail=detail,
            )
        )
    return statuses


def tool_status() -> dict[str, bool]:
    return {
        "ansible": shutil.which("ansible") is not None,
        "ssh": shutil.which("ssh") is not None,
        "git": shutil.which("git") is not None,
        "python3": shutil.which("python3") is not None,
    }
