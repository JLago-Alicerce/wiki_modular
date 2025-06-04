from pathlib import Path
import yaml
import re
import unicodedata

def normalize_slug(text: str) -> str:
    """
    Convierte el texto a un slug más robusto:
      - Elimina acentos y diacríticos.
      - Sustituye caracteres no alfanuméricos (excepto guiones y espacios) por nada.
      - Reemplaza secuencias de espacios y guiones por un solo guion bajo.
      - Retorna todo en minúsculas.
    """
    # Normalizar a forma NFKD (descompone acentos)
    normalized = unicodedata.normalize('NFKD', text)
    # Convertir a ASCII ignorando caracteres no mapeables
    ascii_text = normalized.encode('ascii', 'ignore').decode('ascii')
    # Eliminar todo lo que no sea alfanumérico, espacio o guion
    ascii_text = re.sub(r'[^a-zA-Z0-9\s-]', '', ascii_text)
    # Reemplazar secuencias de espacios o guiones por un solo "_"
    ascii_text = re.sub(r'[\s-]+', '_', ascii_text)
    # Convertir a minúsculas
    return ascii_text.lower()

def generate_map_from_markdown(md_path: Path, yaml_path: Path) -> None:
    """
    Lee un archivo Markdown y genera un archivo YAML que describe sus encabezados (H1 a H5).
    
    Por cada encabezado detectado se incluye:
      - h_level: nivel de encabezado (1 a 5).
      - titulo:  texto crudo del encabezado.
      - ruta:    un slug derivado del título (campo 'ruta' para indexado futuro).
      - start_line: línea donde comienza el bloque.
      - end_line:   línea donde termina el bloque (calculada a partir del siguiente encabezado).
    
    :param md_path:   Ruta al archivo Markdown fuente.
    :param yaml_path: Ruta donde se escribirá el mapa en formato YAML.
    """
    # Leer el contenido del archivo .md línea a línea
    lines = md_path.read_text(encoding="utf-8").splitlines()

    # Detectar encabezados H1 a H5
    mapa = []
    for i, line in enumerate(lines):
        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            # Verificar si es un nivel entre H1 y H5
            if 1 <= level <= 5:
                raw_title = line[level:].strip()
                # Generar slug a partir del título
                slug = normalize_slug(raw_title)
                mapa.append({
                    "h_level": level,
                    "titulo": raw_title,
                    "ruta": f"{slug}.md",
                    "start_line": i + 1
                })

    # Calcular línea de fin de cada bloque
    for idx in range(len(mapa) - 1):
        mapa[idx]["end_line"] = mapa[idx + 1]["start_line"] - 1
    if mapa:
        mapa[-1]["end_line"] = len(lines)

    # Guardar el resultado en YAML
    yaml_path.write_text(
        yaml.dump(mapa, allow_unicode=True),
        encoding="utf-8"
    )
    print(f"Mapa generado con {len(mapa)} bloques detectados (niveles H1 a H5).")

if __name__ == "__main__":
    # Rutas de ejemplo
    md_path = Path("_fuentes/tmp_full.md")
    yaml_path = Path("_fuentes/mapa_encabezados.yaml")
    
    generate_map_from_markdown(md_path, yaml_path)
