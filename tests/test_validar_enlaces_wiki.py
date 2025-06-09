import csv
from pathlib import Path

from scripts import validar_enlaces_wiki as val


def setup_env(tmp_path: Path):
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    sidebar = wiki / "_sidebar.md"
    return wiki, sidebar


def test_valida_sin_errores(tmp_path, monkeypatch):
    wiki, sidebar = setup_env(tmp_path)
    (wiki / "a.md").write_text("contenido", encoding="utf-8")
    sidebar.write_text("* [A](a.md)\n", encoding="utf-8")

    monkeypatch.setattr(val, "ROOT", tmp_path)
    monkeypatch.setattr(val, "WIKI_DIR", wiki)
    monkeypatch.setattr(val, "SIDEBAR", sidebar)

    assert val.main() == 0
    assert not (tmp_path / "mismatch_report.csv").exists()


def test_detecta_links_invalidos(tmp_path, monkeypatch):
    wiki, sidebar = setup_env(tmp_path)
    (wiki / "a.md").write_text("[bad](/missing.md)", encoding="utf-8")
    sidebar.write_text("* [A](a.md)\n* [Falta](no.md)\n", encoding="utf-8")

    monkeypatch.setattr(val, "ROOT", tmp_path)
    monkeypatch.setattr(val, "WIKI_DIR", wiki)
    monkeypatch.setattr(val, "SIDEBAR", sidebar)
    result = val.main()
    assert result == 1
    report = tmp_path / "mismatch_report.csv"
    rows = list(csv.DictReader(report.open()))
    assert len(rows) == 2
    assert rows[0]["origen"] == "_sidebar.md"
    assert rows[0]["enlace"].startswith("no")
    assert rows[1]["origen"] == "a.md"
