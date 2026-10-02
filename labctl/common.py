from __future__ import annotations

import os
from pathlib import Path

PROJECT_ENV = "RHCSA_LAB_ROOT"

def project_root() -> Path:
    override = os.environ.get(PROJECT_ENV)
    if override:
        return Path(override).expanduser().resolve()

    # labctl/common.py -> project root
    return Path(__file__).resolve().parent.parent

def ansible_dir() -> Path:
    return project_root() / "ansible"

def labs_dir() -> Path:
    return project_root() / "labs"
