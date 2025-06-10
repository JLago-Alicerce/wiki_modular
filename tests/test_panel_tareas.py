import sys

from scripts import panel_tareas


def reload_panel():
    import importlib

    import wiki_modular.history as hist

    importlib.reload(hist)
    importlib.reload(panel_tareas)
    return panel_tareas


def test_panel_workflow(tmp_path, monkeypatch, capsys):
    logs = tmp_path / "logs"
    monkeypatch.setenv("WM_LOGS_DIR", str(logs))
    mod = reload_panel()

    # run a simple command
    monkeypatch.setattr(
        sys, "argv", ["prog", "run", sys.executable, "-c", 'print("ok")']
    )
    mod.main()
    run_id = next(logs.glob("*.log")).stem

    # list should include the run id
    monkeypatch.setattr(sys, "argv", ["prog", "list"])
    mod.main()
    out = capsys.readouterr().out
    assert run_id in out

    # show should display log content
    monkeypatch.setattr(sys, "argv", ["prog", "show", run_id])
    mod.main()
    out = capsys.readouterr().out
    assert "ok" in out

    # repeat should create another log
    monkeypatch.setattr(sys, "argv", ["prog", "repeat"])
    mod.main()
    out = capsys.readouterr().out
    assert "Nueva ejecuci" in out
    assert len(list(logs.glob("*.log"))) == 2
