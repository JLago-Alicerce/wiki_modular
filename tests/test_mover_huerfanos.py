import csv
from pathlib import Path
import yaml
from scripts import mover_huerfanos as mover


def create_files(tmp_path: Path):
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    (wiki / "README.md").write_text("doc", encoding="utf-8")
    (wiki / "1_intro.md").write_text("intro", encoding="utf-8")
    inst = wiki / "02_Instancias_SQL"
    inst.mkdir()
    (inst / "sql.md").write_text("sql", encoding="utf-8")
    (wiki / "extra.md").write_text("extra", encoding="utf-8")
    sidebar = wiki / "_sidebar.md"
    sidebar.write_text(
        "* [Intro](1_intro.md)\n  * [SQL](02_Instancias_SQL/sql.md)", encoding="utf-8"
    )
    index = tmp_path / "index_PlataformaBBDD.yaml"
    data = {"secciones": [{"titulo": "Intro", "id": 1, "subtemas": ["SQL"]}]}
    index.write_text(yaml.safe_dump(data), encoding="utf-8")
    return wiki, sidebar, index


def test_move_orphans(tmp_path, monkeypatch):
    wiki, sidebar, index = create_files(tmp_path)

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(mover, "ROOT_DIR", tmp_path)
    monkeypatch.setattr(mover, "WIKI_DIR", wiki)
    monkeypatch.setattr(mover, "INDEX_FILE", index)
    monkeypatch.setattr(mover, "SIDEBAR_FILE", sidebar)
    monkeypatch.setattr(mover, "DEPRECATED_DIR", wiki / "_deprecated")
    monkeypatch.setattr(mover, "CSV_REPORT", tmp_path / "orphaned_files.csv")

    mover.main()

    moved = wiki / "_deprecated" / "extra.md"
    assert moved.exists()
    assert not (wiki / "extra.md").exists()

    rows = list(csv.DictReader((tmp_path / "orphaned_files.csv").open()))
    assert rows[0]["file"].endswith("extra.md")
    assert rows[0]["moved_to"].endswith("_deprecated/extra.md")
