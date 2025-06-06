import csv
import pytest

from scripts import auditar_sidebar_vs_fs as audit


def test_auditar_sidebar_empty(tmp_path, monkeypatch):
    root = tmp_path
    sidebar = root / "wiki/_sidebar.md"
    sidebar.parent.mkdir(parents=True)
    sidebar.write_text("", encoding="utf-8")
    wiki = root / "wiki"
    wiki.mkdir(exist_ok=True)

    monkeypatch.setattr(audit, "ROOT", root)
    monkeypatch.setattr(audit, "SIDEBAR", sidebar)
    monkeypatch.setattr(audit, "WIKI_DIR", wiki)

    with pytest.raises(SystemExit) as exc:
        audit.main()
    assert exc.value.code == 1

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
