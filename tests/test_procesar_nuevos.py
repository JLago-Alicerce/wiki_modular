import sys
import subprocess
from pathlib import Path

import pytest

from scripts import procesar_nuevos as pn
from scripts import wiki_cli


def test_run_pipeline_aborts_on_error(monkeypatch):
    cmds = []
    monkeypatch.setattr(
        pn,
        "PIPELINE",
        [lambda d: ["cmd1"], lambda d: ["cmd2"]],
    )

    def fake_run(cmd):
        cmds.append(cmd)
        rc = 0 if cmd == ["cmd1"] else 1
        return subprocess.CompletedProcess(cmd, rc)

    monkeypatch.setattr(subprocess, "run", fake_run)

    with pytest.raises(RuntimeError):
        pn.run_pipeline(Path("doc.docx"))

    assert cmds == [["cmd1"], ["cmd2"]]


def test_convertir_pdf_error_on_extract(tmp_path, monkeypatch):
    pdf = tmp_path / "file.pdf"
    pdf.write_text("data", encoding="utf-8")

    errors = tmp_path / "errores.csv"
    monkeypatch.setattr(pn, "PDF_ERRORS", errors)

    def fake_extract(_):
        raise ValueError("fail")

    monkeypatch.setattr(pn, "extract_text", fake_extract)

    result = pn.convertir_pdf(pdf)

    assert result is None
    assert errors.exists()
    content = errors.read_text(encoding="utf-8").strip().split(",")
    assert content[0] == "file.pdf"


def test_wiki_cli_full_flow(tmp_path, monkeypatch):
    doc = tmp_path / "doc.docx"
    doc.write_text("dummy", encoding="utf-8")

    calls = []

    def fake_run(cmd):
        calls.append(cmd)
        return None

    monkeypatch.setattr(wiki_cli, "run", fake_run)
    monkeypatch.setattr(sys, "argv", ["prog", "full", str(doc), "--cutoff", "0.3"])

    wiki_cli.main()

    names = []
    for cmd in calls:
        if cmd[0] == "pandoc":
            names.append("pandoc")
        else:
            names.append(Path(cmd[1]).name)

    assert names == [
        "resetear_entorno.py",
        "normalizar_estilos_docx.py",
        "pandoc",
        "limpiar_md.py",
        "generar_mapa_encabezados.py",
        "generar_index_desde_encabezados.py",
        "ingest_wiki_v2.py",
        "generar_sidebar.py",
        "auditar_sidebar_vs_fs.py",
    ]
    assert len(calls) == 9
