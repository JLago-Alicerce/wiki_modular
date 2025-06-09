import subprocess
from pathlib import Path
from scripts import iniciar_entorno as start


def test_main_runs_pipelines(tmp_path, monkeypatch):
    orig = tmp_path / "_fuentes" / "_originales"
    orig.mkdir(parents=True)

    docx = orig / "doc.docx"
    docx.write_text("dummy", encoding="utf-8")
    pdf = orig / "file.pdf"
    pdf.write_text("dummy", encoding="utf-8")

    pdf_called = {}
    docx_called = {}

    def fake_run(cmd):
        return subprocess.CompletedProcess(cmd, 0)

    def fake_convert(path, *, ocr=False, dest=None):
        pdf_called["file"] = path
        return dest or tmp_path / "tmp.md"

    def fake_pipeline(path, *, skip_pandoc=False):
        if skip_pandoc:
            pdf_called["pipeline"] = path
        else:
            docx_called["pipeline"] = path

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(start, "run", lambda cmd: None)
    monkeypatch.setattr(start.pn, "convertir_pdf", fake_convert)
    monkeypatch.setattr(start.pn, "run_pipeline", fake_pipeline)

    start.main()

    assert pdf_called["file"].resolve() == pdf
    assert pdf_called["pipeline"].resolve() == pdf
    assert docx_called["pipeline"].resolve() == docx
