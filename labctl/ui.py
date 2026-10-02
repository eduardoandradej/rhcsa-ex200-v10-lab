from __future__ import annotations

import os
import sys

USE_COLOR = sys.stdout.isatty() and "NO_COLOR" not in os.environ

def _wrap(code: str, value: str) -> str:
    if not USE_COLOR:
        return value
    return f"\033[{code}m{value}\033[0m"

def bold(value: str) -> str:
    return _wrap("1", value)

def green(value: str) -> str:
    return _wrap("32", value)

def red(value: str) -> str:
    return _wrap("31", value)

def yellow(value: str) -> str:
    return _wrap("33", value)

def cyan(value: str) -> str:
    return _wrap("36", value)

def dim(value: str) -> str:
    return _wrap("2", value)

def rule(width: int = 72) -> str:
    return "─" * width
