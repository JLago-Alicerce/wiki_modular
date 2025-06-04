.PHONY: all map index sidebar audit build

map:
python scripts/generar_mapa_encabezados.py

index:
python scripts/generar_index_desde_encabezados.py

sidebar:
python scripts/generar_sidebar_desde_index.py

audit:
python scripts/auditar_sidebar_vs_fs.py

all: map index sidebar

build: all audit
