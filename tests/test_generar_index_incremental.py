import yaml
from scripts.generar_index_desde_encabezados import generar_indice


def test_generar_indice_incremental(tmp_path):
    mapa = [{"titulo": "Nueva"}]
    input_file = tmp_path / "mapa.yaml"
    input_file.write_text(yaml.safe_dump(mapa), encoding="utf-8")

    existente = {
        "secciones": [
            {"id": 5, "titulo": "Prev", "slug": "prev", "subtemas": ["uno"]}
        ]
    }
    index_file = tmp_path / "index.yaml"
    index_file.write_text(yaml.safe_dump(existente), encoding="utf-8")

    generar_indice(input_file, index_file)
    data = yaml.safe_load(index_file.read_text(encoding="utf-8"))

    assert len(data["secciones"]) == 2
    assert data["secciones"][0]["subtemas"] == ["uno"]
    assert data["secciones"][1]["id"] == 6
    assert data["secciones"][1]["titulo"] == "Nueva"
