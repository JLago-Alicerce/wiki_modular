import wiki_modular
import yaml
import pytest


def test_load_yaml_parses_valid(tmp_path):
    data = {'key': 'value', 'list': [1, 2]}
    file = tmp_path / 'sample.yaml'
    file.write_text(yaml.safe_dump(data), encoding='utf-8')
    assert wiki_modular.load_yaml(file) == data


def test_load_yaml_missing_file(tmp_path):
    missing = tmp_path / 'missing.yaml'
    with pytest.raises(FileNotFoundError):
        wiki_modular.load_yaml(missing)
