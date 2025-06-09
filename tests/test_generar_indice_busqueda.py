import json
import sys
from pathlib import Path
import yaml

import scripts.generar_indice_busqueda as gen


def test_generar_indice_creates_json(tmp_path, monkeypatch):
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    md = wiki / "sample.md"
    md.write_text("---\nsource: doc.docx\nextra: 1\n---\n\ncontenido", encoding="utf-8")

    out = tmp_path / "index.json"
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog", "--wiki", str(wiki), "--output", str(out)])
    gen.main()

    data = json.loads(out.read_text(encoding="utf-8"))
    assert isinstance(data, list)
    assert data[0]["path"] == "sample.md"
    assert data[0]["metadata"]["source"] == "doc.docx"
    assert "contenido" in data[0]["content"]
