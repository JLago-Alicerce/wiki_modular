#!/usr/bin/env python
"""Gestiona historial de ejecuci\u00f3n de comandos."""
from __future__ import annotations

import argparse
from pathlib import Path

from wiki_modular.history import last_entry, log_run, read_history


def cmd_list() -> None:
    """Mostrar tabla con ejecuciones pasadas."""
    history = read_history()
    if not history:
        print("No hay ejecuciones registradas")
        return
    print(f"{'ID':<17} {'Duración(s)':>12} Estado")
    for e in history:
        print(f"{e.id:<17} {e.duration:>12.1f} {e.status}")


def cmd_show(run_id: str) -> None:
    """Imprimir el log asociado a ``run_id``."""
    history = {e.id: e for e in read_history()}
    entry = history.get(run_id)
    if not entry:
        print(f"No se encontr\u00f3 la ejecuci\u00f3n {run_id}")
        return
    path = Path(entry.log)
    if not path.exists():
        print(f"Log no disponible: {path}")
        return
    print(path.read_text(encoding="utf-8"))


def cmd_run(args: list[str]) -> None:
    """Ejecutar ``args`` registrando salida y duraci\u00f3n."""
    if not args:
        print("Debe indicar el comando a ejecutar")
        return
    entry = log_run(args)
    print(f"Ejecuci\u00f3n registrada con ID {entry.id}")


def cmd_repeat() -> None:
    """Repetir la \u00faltima tarea registrada."""
    entry = last_entry()
    if not entry:
        print("No hay tareas previas para repetir")
        return
    print(f"Repitiendo: {' '.join(entry.command)}")
    new_entry = log_run(entry.command)
    print(f"Nueva ejecuci\u00f3n registrada con ID {new_entry.id}")


def main() -> None:
    """Punto de entrada principal."""
    parser = argparse.ArgumentParser(description="Panel de tareas")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list", help="Mostrar historial")

    show_p = sub.add_parser("show", help="Ver log de una ejecuci\u00f3n")
    show_p.add_argument("id")

    run_p = sub.add_parser("run", help="Ejecutar y registrar")
    run_p.add_argument("command", nargs=argparse.REMAINDER)

    sub.add_parser("repeat", help="Repetir \u00faltima tarea")

    ns = parser.parse_args()

    if ns.cmd == "list":
        cmd_list()
    elif ns.cmd == "show":
        cmd_show(ns.id)
    elif ns.cmd == "run":
        cmd_run(ns.command)
    elif ns.cmd == "repeat":
        cmd_repeat()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
