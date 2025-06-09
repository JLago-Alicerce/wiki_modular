import yaml
from scripts.generar_index_desde_encabezados import generar_indice
from scripts.verificar_pre_ingesta import main as precheck


def test_precheck_ignore_extra(tmp_path):
    mapa_file = tmp_path / 'mapa.yaml'
    mapa_file.write_text(yaml.safe_dump([{'titulo': 'Nueva'}]), encoding='utf-8')

    index_file = tmp_path / 'index.yaml'
    index_file.write_text(
        yaml.safe_dump({'secciones': [{'id': 1, 'titulo': 'Prev', 'slug': 'prev', 'subtemas': []}]}),
        encoding='utf-8'
    )

    generar_indice(mapa_file, index_file)

    rc = precheck(str(mapa_file), str(index_file), ignore_extra=True)
    assert rc == 0
