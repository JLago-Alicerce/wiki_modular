import subprocess
from pathlib import Path
from scripts import resetear_entorno as reset


def test_preserve_readme(tmp_path, monkeypatch):
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    readme = wiki / "README.md"
    readme.write_text("contenido", encoding="utf-8")
    extra = wiki / "extra.md"
    extra.write_text("data", encoding="utf-8")

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(reset, "RUTAS", [Path("wiki")])

    reset.main()

    assert readme.exists()
    assert not extra.exists()
