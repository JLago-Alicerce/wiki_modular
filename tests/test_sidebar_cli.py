import yaml
import sys
from pathlib import Path
from scripts import generar_sidebar_desde_index as gen


def test_main_respects_cli_paths(tmp_path, monkeypatch):
    index_file = tmp_path / 'idx.yaml'
    index_file.write_text(yaml.safe_dump({'secciones': [{'titulo': 'Intro'}]}), encoding='utf-8')
    out_file = tmp_path / 'sidebar.md'

    monkeypatch.setattr(sys, 'argv', ['prog', '--index', str(index_file), '--out', str(out_file)])
    gen.main()

    assert out_file.exists()
    content = out_file.read_text(encoding='utf-8').splitlines()
    assert content[0] == '* [Inicio](README.md)'
