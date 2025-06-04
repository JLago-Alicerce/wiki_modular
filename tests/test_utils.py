import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from scripts.utils import normalize_slug


def test_normalize_slug_basic():
    assert normalize_slug('Hola Mundo') == 'hola_mundo'


def test_normalize_slug_accents():
    assert normalize_slug('Árbol de decisión') == 'arbol_de_decision'


def test_normalize_slug_symbols():
    assert normalize_slug('A/B & C?') == 'ab_c'
