import csv

from scripts import auditar_sidebar_vs_fs as audit


def test_auditar_sidebar_empty(tmp_path, monkeypatch):
    root = tmp_path
    wiki = root / "wiki"
    wiki.mkdir()
    sidebar = wiki / "_sidebar.md"
    sidebar.write_text("", encoding="utf-8")

    monkeypatch.setattr(audit, "ROOT", root)
    monkeypatch.setattr(audit, "SIDEBAR", sidebar)
    monkeypatch.setattr(audit, "WIKI_DIR", wiki)

    audit.main()

    report = root / "mismatch_report.csv"
    assert report.exists()
    rows = list(csv.reader(report.open()))
    assert rows[0] == [
        "enlace_sidebar",
        "coincidencia_fs",
        "slug_sidebar",
        "slug_fs",
        "status",
    ]
