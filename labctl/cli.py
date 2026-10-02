from __future__ import annotations

import argparse
from pathlib import Path
import sys

from . import __version__
from .catalog import discover_labs, by_objective, find_lab
from .runner import run_grader, run_playbook
from .state import clear_active, load_active, save_active, update_score
from .status import node_statuses, tool_status
from .ui import bold, cyan, dim, green, red, yellow, rule


LOCAL_PLATFORM = "RHEL 9.8"
EXAM_TARGET = "RHEL 10"


def stars(value: int) -> str:
    value = max(1, min(5, value))
    return "★" * value


def _prompt_path(lab, lang: str) -> Path:
    return lab.path / f"prompt.{lang}.md"


def _read_prompt(lab, lang: str) -> str:
    path = _prompt_path(lab, lang)
    if not path.exists() and lang != "pt":
        path = _prompt_path(lab, "pt")
    if not path.exists():
        return "Enunciado ainda não disponível."
    return path.read_text(encoding="utf-8").strip()


def _resolve_lab(lab_id: str | None):
    if lab_id:
        lab = find_lab(lab_id)
        if lab is None:
            raise ValueError(f"Laboratório não encontrado: {lab_id}")
        return lab

    active = load_active()
    if not active:
        raise ValueError("Nenhum laboratório ativo.")

    lab = find_lab(active["lab_id"])
    if lab is None:
        raise ValueError(
            f"O estado aponta para um laboratório inexistente: {active['lab_id']}"
        )
    return lab


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

    active = load_active()
    print()
    print(bold("Lab State"))
    if active:
        print(f"  Active      {active.get('lab_id')}")
        if active.get("last_score") is not None:
            print(f"  Last score  {active.get('last_score')}%")
    else:
        print("  Active      none")

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
        print(f"{'ID':<11} {'LAB':<34} {'LEVEL':<7} {'TIME':>5}  {'STATUS'}")
        print("─" * 78)
        for lab in objective_labs:
            print(
                f"{lab.id:<11} "
                f"{lab.title:<34.34} "
                f"{stars(lab.difficulty):<7} "
                f"{str(lab.duration) + 'm':>5}  "
                f"{lab.status}"
            )
        print()

    print(dim(f"Total: {len(labs)} laboratório(s)"))
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    try:
        lab = _resolve_lab(args.lab_id)
    except Exception as exc:
        print(red(str(exc)))
        print("Use: lab list")
        return 2

    title = lab.title_en if args.lang == "en" else lab.title

    print(bold("RHCSA EX200 Lab"))
    print(rule())
    print()
    print(f"{'ID':<14}{lab.id}")
    print(f"{'Objective':<14}{lab.objective}")
    print(f"{'Title':<14}{title}")
    print()
    print(f"{'Target':<14}{', '.join(lab.targets)}")
    print(f"{'Difficulty':<14}{stars(lab.difficulty)}")
    print(f"{'Time':<14}{lab.duration} minutes")
    print()
    print(bold("Compatibility"))
    print(f"  Local       {lab.compatibility_local}")
    print(f"  Target      {lab.compatibility_target}")
    print(f"  Level       {lab.compatibility_level}")
    print()
    print(f"{'Reset policy':<14}{lab.reset_policy}")
    print(f"{'Status':<14}{lab.status}")
    print()
    print(bold("Description" if args.lang == "en" else "Descrição"))
    print(_read_prompt(lab, args.lang))
    return 0


def cmd_start(args: argparse.Namespace) -> int:
    try:
        lab = _resolve_lab(args.lab_id)
    except Exception as exc:
        print(red(str(exc)))
        return 2

    if lab.status != "ready":
        print(yellow(
            f"{lab.id} ainda está em estado '{lab.status}'. "
            "Este laboratório não pode ser iniciado."
        ))
        return 2

    active = load_active()
    if active:
        print(yellow(
            f"Já existe um laboratório ativo: {active.get('lab_id')}. "
            "Finalize-o com 'lab finish' antes de iniciar outro."
        ))
        return 2

    setup = lab.path / "setup.yml"
    if not setup.exists():
        print(red(f"setup.yml não encontrado para {lab.id}"))
        return 2

    print(f"Preparing {lab.id}...")
    proc = run_playbook(setup)

    if proc.returncode != 0:
        print(red("Falha ao preparar o laboratório."))
        if proc.stdout:
            print(proc.stdout.rstrip())
        if proc.stderr:
            print(proc.stderr.rstrip())
        return proc.returncode or 2

    save_active(lab.id, lab.targets)

    print(green("LAB READY"))
    print(rule())
    print(f"Objective : {lab.objective}")
    print(f"Exercise  : {lab.title}")
    print(f"Target    : {', '.join(lab.targets)}")
    print(f"Time      : {lab.duration} minutes")
    print(f"RHEL 9.8  : {lab.compatibility_level}")
    print("RHEL 10   : target")
    print()
    print(bold("Tarefa"))
    print(_read_prompt(lab, args.lang))
    print()
    print(f"Conecte-se: ssh student@{lab.targets[0]}")
    print(f"Quando terminar: lab grade {lab.id}")
    return 0


def cmd_grade(args: argparse.Namespace) -> int:
    try:
        lab = _resolve_lab(args.lab_id)
    except Exception as exc:
        print(red(str(exc)))
        return 2

    active = load_active()
    if not active or active.get("lab_id") != lab.id:
        print(yellow(
            f"{lab.id} não é o laboratório ativo. "
            "Inicie-o primeiro com 'lab start'."
        ))
        return 2

    grader = lab.path / "grade.py"
    if not grader.exists():
        print(red(f"grade.py não encontrado para {lab.id}"))
        return 2

    try:
        _rc, payload = run_grader(grader)
    except Exception as exc:
        print(red(f"Falha no grader: {exc}"))
        return 2

    checks = payload.get("checks", [])
    score = int(payload.get("score", 0))

    print(bold(f"Grade — {lab.id}"))
    print(rule())

    for check in checks:
        ok = bool(check.get("pass"))
        label = str(check.get("label", "check"))
        prefix = green("[PASS]") if ok else red("[FAIL]")
        print(f"{prefix} {label}")
        if not ok and check.get("hint"):
            print(dim(f"       dica: {check['hint']}"))

    print()
    print(f"Score: {score}%")
    update_score(score)

    if score == 100:
        print(green("Resultado: PASS"))
        return 0

    print(yellow("Resultado: INCOMPLETE"))
    return 1


def cmd_finish(args: argparse.Namespace) -> int:
    try:
        lab = _resolve_lab(args.lab_id)
    except Exception as exc:
        print(red(str(exc)))
        return 2

    active = load_active()
    if not active or active.get("lab_id") != lab.id:
        print(yellow(f"{lab.id} não é o laboratório ativo."))
        return 2

    finish = lab.path / "finish.yml"
    if not finish.exists():
        print(red(f"finish.yml não encontrado para {lab.id}"))
        return 2

    print(f"Cleaning {lab.id}...")
    proc = run_playbook(finish)

    if proc.returncode != 0:
        print(red("Falha ao limpar o laboratório."))
        if proc.stdout:
            print(proc.stdout.rstrip())
        if proc.stderr:
            print(proc.stderr.rstrip())
        return proc.returncode or 2

    clear_active()
    print(green("LAB FINISHED"))
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

    show_parser = sub.add_parser("show", help="mostra detalhes de um laboratório")
    show_parser.add_argument("lab_id", help="ID do laboratório, ex.: obj01-03")
    show_parser.add_argument(
        "--lang",
        choices=("pt", "en"),
        default="pt",
        help="idioma do enunciado (padrão: pt)",
    )
    show_parser.set_defaults(func=cmd_show)

    start_parser = sub.add_parser("start", help="prepara e inicia um laboratório")
    start_parser.add_argument("lab_id", help="ID do laboratório")
    start_parser.add_argument(
        "--lang",
        choices=("pt", "en"),
        default="pt",
        help="idioma do enunciado (padrão: pt)",
    )
    start_parser.set_defaults(func=cmd_start)

    grade_parser = sub.add_parser("grade", help="avalia o laboratório ativo")
    grade_parser.add_argument("lab_id", nargs="?", help="ID; omita para usar o ativo")
    grade_parser.set_defaults(func=cmd_grade)

    finish_parser = sub.add_parser("finish", help="limpa e finaliza o laboratório ativo")
    finish_parser.add_argument("lab_id", nargs="?", help="ID; omita para usar o ativo")
    finish_parser.set_defaults(func=cmd_finish)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
