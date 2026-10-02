from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import yaml

from .common import labs_dir


@dataclass(frozen=True)
class Lab:
    id: str
    title: str
    objective: str
    targets: tuple[str, ...]
    difficulty: int
    duration: int
    compatibility_level: str
    path: Path


def _load_lab(path: Path) -> Lab:
    with path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}

    required = ("id", "title", "objective", "target", "difficulty", "duration", "compatibility")
    missing = [key for key in required if key not in raw]
    if missing:
        raise ValueError(f"{path}: campos ausentes: {', '.join(missing)}")

    targets = raw["target"]
    if isinstance(targets, str):
        targets = [targets]

    compatibility = raw.get("compatibility") or {}

    return Lab(
        id=str(raw["id"]),
        title=str(raw["title"]),
        objective=str(raw["objective"]),
        targets=tuple(str(x) for x in targets),
        difficulty=int(raw["difficulty"]),
        duration=int(raw["duration"]),
        compatibility_level=str(compatibility.get("level", "unknown")),
        path=path.parent,
    )


def discover_labs() -> list[Lab]:
    root = labs_dir()
    labs: list[Lab] = []

    if not root.exists():
        return labs

    for path in sorted(root.glob("*/*/lab.yml")):
        labs.append(_load_lab(path))

    return labs


def by_objective(labs: Iterable[Lab]) -> dict[str, list[Lab]]:
    result: dict[str, list[Lab]] = {}
    for lab in labs:
        result.setdefault(lab.objective, []).append(lab)
    return result
