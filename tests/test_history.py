import sys
from pathlib import Path

from wiki_modular import history


def reload_history():
    import importlib

    importlib.reload(history)
    return history


def test_log_and_read(tmp_path, monkeypatch):
    monkeypatch.setenv("WM_LOGS_DIR", str(tmp_path))
    mod = reload_history()
    entry = mod.log_run([sys.executable, "-c", 'print("hi")'])

    log_file = Path(entry.log)
    assert log_file.exists()
    assert "hi" in log_file.read_text(encoding="utf-8")

    history = mod.read_history()
    assert len(history) == 1
    assert history[0].id == entry.id
    assert mod.last_entry().id == entry.id
