import wiki_modular


def test_limpiar_slug_basic():
    assert wiki_modular.limpiar_slug("Título de Prueba") == "titulo_de_prueba"
    assert wiki_modular.limpiar_slug("áéíóú") == "aeiou"
    assert wiki_modular.limpiar_slug("Espacios   multiples") == "espacios_multiples"


def test_limpiar_slug_non_ascii():
    assert wiki_modular.limpiar_slug("Sección/Especial") == "seccion_especial"


def test_limpiar_slug_toc():
    assert wiki_modular.limpiar_slug("#_Toc9876 Sección") == "seccion"


def test_remover_indice_markdown(tmp_path):
    md = tmp_path / "doc.md"
    md.write_text(
        """# Título

## Índice de contenidos

1 Introducción........1
1.1 Detalle...........2

## Otra sección
Texto
""",
        encoding="utf-8",
    )
    wiki_modular.limpiar_archivo_markdown(md)
    result = md.read_text(encoding="utf-8")
    assert "Índice de contenidos" not in result
    assert "Introducción" not in result
    assert "Otra sección" in result
