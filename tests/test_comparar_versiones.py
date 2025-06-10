import sys

import scripts.comparar_versiones as cv


def test_make_diff_html_contains_table():
    html = cv.make_diff_html("a", "b")
    assert '<table class="diff"' in html


def test_main_generates_file(tmp_path, monkeypatch):
    old = tmp_path / "old.md"
    new = tmp_path / "new.md"
    out = tmp_path / "diff.html"
    old.write_text("hola", encoding="utf-8")
    new.write_text("adios", encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["prog", str(new), "--backup", str(old), "--out", str(out), "--no-open"],
    )
    cv.main()
    assert out.exists()
