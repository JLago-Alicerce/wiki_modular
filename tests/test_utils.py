import wiki_modular


def test_limpiar_slug_basic():
    assert wiki_modular.limpiar_slug("Título de Prueba") == "titulo_de_prueba"
    assert wiki_modular.limpiar_slug("áéíóú") == "aeiou"
    assert wiki_modular.limpiar_slug("Espacios   multiples") == "espacios_multiples"

def test_limpiar_slug_non_ascii():
    assert wiki_modular.limpiar_slug("Sección/Especial") == "seccion_especial"
