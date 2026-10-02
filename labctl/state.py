from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path

from .common import project_root


def state_dir() -> Path:
    path = project_root() / ".state"
    path.mkdir(parents=True, exist_ok=True)
    return path


def active_path() -> Path:
    return state_dir() / "active.json"


def load_active() -> dict | None:
    path = active_path()
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def save_active(lab_id: str, targets: tuple[str, ...]) -> dict:
    data = {
        "lab_id": lab_id,
        "targets": list(targets),
        "started_at": datetime.now(timezone.utc).isoformat(),
        "last_score": None,
    }
    active_path().write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return data


def update_score(score: int) -> None:
    data = load_active()
    if not data:
        return
    data["last_score"] = score
    active_path().write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def clear_active() -> None:
    path = active_path()
    if path.exists():
        path.unlink()
