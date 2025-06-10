import json
import sys

import scripts.generar_indice_busqueda as gen


def test_generar_indice_creates_json(tmp_path, monkeypatch):
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    md = wiki / "sample.md"
    md.write_text(
        "---\nsource: doc.docx\nextra: 1\n---\n\n## Intro\ntexto\n### Sub\n",
        encoding="utf-8",
    )

    out = tmp_path / "index.json"
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        sys, "argv", ["prog", "--wiki", str(wiki), "--output", str(out)]
    )
    gen.main()

    data = json.loads(out.read_text(encoding="utf-8"))
    assert "sample.md" in data
    assert data["sample.md"]["metadata"]["source"] == "doc.docx"
    assert "Intro" in data["sample.md"]["content"]
    headers = data["sample.md"]["headers"]
    assert {"level": 2, "text": "Intro", "slug": "intro"} in headers
    assert {"level": 3, "text": "Sub", "slug": "sub"} in headers
