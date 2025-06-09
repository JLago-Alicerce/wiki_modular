import scripts.ingest_wiki_v2 as ingest
from pathlib import Path
import yaml
import sys


def sample_index():
    return {
        "secciones": [
            {
                "id": 1,
                "titulo": "Introducción",
                "slug": "intro",
                "subtemas": ["Instalación SQL", "Server"],
            }
        ]
    }


def test_buscar_destino_alias():
    index = sample_index()
    alias = {"Otro": "wiki/custom.md"}
    dest = ingest.buscar_destino("Otro", index, alias, 0.5)
    assert dest == Path("wiki/custom.md")


def test_buscar_destino_exact_and_subtema():
    index = sample_index()
    dest1 = ingest.buscar_destino("Introducción", index, {}, 0.5)
    assert dest1 == Path("wiki/1_intro.md")
    dest2 = ingest.buscar_destino("Instalación SQL", index, {}, 0.5)
    assert dest2 == Path("wiki/02_Instancias_SQL/instalacion_sql.md")


def test_buscar_destino_fuzzy_and_none():
    index = sample_index()
    dest = ingest.buscar_destino("Intrduccion", index, {}, 0.5)
    assert dest == Path("wiki/1_intro.md")
    assert ingest.buscar_destino("Desconocido", index, {}, 0.5) is None


def test_limpiar_nombre_archivo_basic():
    first = ingest.limpiar_nombre_archivo("1. Título *Especial*")
    assert first == "Titulo_Especial"
    second = ingest.limpiar_nombre_archivo("   Ámbito / General  ")
    assert second == "Ambito_General"
    long = "a" * 200
    assert len(ingest.limpiar_nombre_archivo(long)) == 128


def test_main_generates_frontmatter(tmp_path, monkeypatch):
    mapa = [{"titulo": "Intro", "start_line": 1, "h_level": 1}]
    mapa_file = tmp_path / "mapa.yaml"
    mapa_file.write_text(yaml.safe_dump(mapa), encoding="utf-8")

    index = {"secciones": [{"id": 1, "titulo": "Intro", "slug": "intro", "subtemas": []}]}
    index_file = tmp_path / "index.yaml"
    index_file.write_text(yaml.safe_dump(index), encoding="utf-8")

    fuente = tmp_path / "full.md"
    fuente.write_text("# Intro\n\ncontenido", encoding="utf-8")

    alias = tmp_path / "alias.yaml"
    alias.write_text("{}", encoding="utf-8")

    monkeypatch.chdir(tmp_path)
    args = [
        "prog",
        "--mapa",
        str(mapa_file),
        "--index",
        str(index_file),
        "--fuente",
        str(fuente),
        "--alias",
        str(alias),
        "--docx",
        "orig.docx",
    ]
    monkeypatch.setattr(sys, "argv", args)
    ingest.main()

    out_file = tmp_path / "wiki" / "1_intro.md"
    text = out_file.read_text(encoding="utf-8")
    assert text.startswith("---")
    parts = text.split("---", 2)
    meta = yaml.safe_load(parts[1])
    assert meta["source"] == "orig.docx"
