import scripts.ingest_wiki_v2 as ingest
from pathlib import Path


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
