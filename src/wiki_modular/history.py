"""Registro de ejecuciones de comandos."""

from __future__ import annotations

import json
import os
import subprocess
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List

LOGS_DIR = Path(os.environ.get("WM_LOGS_DIR", "logs"))
HISTORY_FILE = LOGS_DIR / "historial.jsonl"


@dataclass
class Entry:
    """Representa la ejecuci\u00f3n de un comando."""

    id: str
    command: List[str]
    start: str
    end: str
    duration: float
    status: str
    log: str


def _write_entry(entry: Entry) -> None:
    LOGS_DIR.mkdir(exist_ok=True)
    with HISTORY_FILE.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")


def read_history() -> List[Entry]:
    """Devuelve la lista de ejecuciones registradas."""
    if not HISTORY_FILE.exists():
        return []
    entries: List[Entry] = []
    for line in HISTORY_FILE.read_text(encoding="utf-8").splitlines():
        try:
            data = json.loads(line)
            entries.append(Entry(**data))
        except Exception:  # noqa: BLE001
            continue
    return entries


def log_run(cmd: Iterable[str]) -> Entry:
    """Ejecuta ``cmd`` registrando duraci\u00f3n y salida."""
    command = list(map(str, cmd))
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S%f")
    log_path = LOGS_DIR / f"{run_id}.log"
    LOGS_DIR.mkdir(exist_ok=True)
    start_time = time.time()
    proc = subprocess.run(command, capture_output=True, text=True)
    end_time = time.time()
    log_path.write_text(proc.stdout + proc.stderr, encoding="utf-8")

    entry = Entry(
        id=run_id,
        command=command,
        start=datetime.fromtimestamp(start_time).isoformat(timespec="seconds"),
        end=datetime.fromtimestamp(end_time).isoformat(timespec="seconds"),
        duration=end_time - start_time,
        status="ok" if proc.returncode == 0 else "fail",
        log=str(log_path),
    )
    _write_entry(entry)
    return entry


def last_entry() -> Entry | None:
    """Devuelve la \u00faltima ejecuci\u00f3n registrada o ``None``."""
    history = read_history()
    return history[-1] if history else None


__all__ = ["log_run", "read_history", "last_entry", "Entry"]
