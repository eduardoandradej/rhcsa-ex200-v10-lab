from __future__ import annotations

import argparse
import sys

from . import __version__
from .catalog import discover_labs, by_objective
from .status import node_statuses, tool_status
from .ui import bold, cyan, dim, green, red, yellow, rule


LOCAL_PLATFORM = "RHEL 9.8"
EXAM_TARGET = "RHEL 10"


def stars(value: int) -> str:
    value = max(1, min(5, value))
    return "★" * value


def cmd_status(_args: argparse.Namespace) -> int:
    print(bold("RHCSA EX200 Lab"))
    print(rule())
    print()

    try:
        nodes = node_statuses()
    except Exception as exc:
        print(red("Falha ao consultar o inventory/Ansible:"))
        print(f"  {exc}")
        return 2

    control = [n for n in nodes if n.role == "control"]
    managed = [n for n in nodes if n.role == "managed"]

    print(bold("Control Plane"))
    for node in control:
        state = green("ONLINE") if node.online else red("OFFLINE")
        print(f"  {node.name:<10} {node.address:<18} {state}")

    print()
    print(bold("Managed Nodes"))
    for node in managed:
        state = green("ONLINE") if node.online else red("OFFLINE")
        print(f"  {node.name:<10} {node.address:<18} {state}")

    print()
    print(bold("Platform"))
    print(f"  Local       {LOCAL_PLATFORM}")
    print(f"  Exam target {EXAM_TARGET}")

    print()
    print(bold("Tooling"))
    tools = tool_status()
    for name in ("ansible", "ssh", "git", "python3"):
        state = green("OK") if tools[name] else red("MISSING")
        print(f"  {name:<10} {state}")

    ready = all(n.online for n in nodes) and all(tools.values())
    print()
    print(f"Environment: {green('READY') if ready else yellow('DEGRADED')}")
    return 0 if ready else 1


def cmd_list(args: argparse.Namespace) -> int:
    try:
        labs = discover_labs()
    except Exception as exc:
        print(red(f"Erro no catálogo: {exc}"))
        return 2

    if args.objective:
        needle = args.objective.lower()
        labs = [
            lab for lab in labs
            if needle in lab.objective.lower() or needle in lab.id.lower()
        ]

    print(bold("RHCSA EX200 v10 Labs"))
    print(dim(f"Execução local: {LOCAL_PLATFORM} | Referência: {EXAM_TARGET}"))
    print()

    if not labs:
        print(yellow("Nenhum laboratório encontrado."))
        return 0

    groups = by_objective(labs)
    for objective, objective_labs in groups.items():
        print(cyan(bold(objective.upper())))
        print()
        print(f"{'ID':<11} {'LAB':<34} {'LEVEL':<7} {'TIME':>5}  {'COMPAT'}")
        print("─" * 76)
        for lab in objective_labs:
            print(
                f"{lab.id:<11} "
                f"{lab.title:<34.34} "
                f"{stars(lab.difficulty):<7} "
                f"{str(lab.duration) + 'm':>5}  "
                f"{lab.compatibility_level}"
            )
        print()

    print(dim(f"Total: {len(labs)} laboratório(s)"))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lab",
        description="RHCSA EX200 local lab controller",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    sub = parser.add_subparsers(dest="command", required=True)

    status_parser = sub.add_parser("status", help="valida o Control Plane e os nós")
    status_parser.set_defaults(func=cmd_status)

    list_parser = sub.add_parser("list", help="lista o catálogo de laboratórios")
    list_parser.add_argument(
        "--objective",
        help="filtra por objetivo ou ID (ex.: essential, obj01)",
    )
    list_parser.set_defaults(func=cmd_list)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
