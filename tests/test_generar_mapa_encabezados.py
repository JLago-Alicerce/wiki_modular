import yaml
from scripts.generar_mapa_encabezados import generate_map_from_markdown


def test_generate_h2_map(tmp_path):
    md = tmp_path / "doc.md"
    md.write_text(
        "# Titulo\n\n## Primero\ntexto\n### Sub\n##Segundo\n", encoding="utf-8"
    )
    out = tmp_path / "mapa.yaml"
    generate_map_from_markdown(md, out)

    mapa = yaml.safe_load(out.read_text(encoding="utf-8"))
    assert [b["titulo"] for b in mapa] == ["Primero", "Segundo"]
    assert mapa[0]["start_line"] == 3
    assert mapa[0]["end_line"] == 5
    assert mapa[1]["start_line"] == 6
    assert mapa[1]["end_line"] == 6
