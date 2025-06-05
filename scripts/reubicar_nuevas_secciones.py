#!/usr/bin/env python3
import os
from pathlib import Path
import shutil
from difflib import SequenceMatcher

# Configuración
root = Path(".")
nuevas_dir = root / "wiki" / "99_Nuevas_Secciones"
destino_base = root / "wiki"
index_file = root / "index_PlataformaBBDD.yaml"

# Cargar índice
import yaml
index_data = yaml.safe_load(index_file.read_text(encoding="utf-8"))

# Normalizador básico
def normalizar(texto):
    import unicodedata
    texto = unicodedata.normalize('NFKD', texto)
    return texto.encode('ascii', 'ignore').decode('ascii').lower().strip()

def main() -> None:
    """Reubica las nuevas secciones según el índice."""
    # Reubicar
    for md in nuevas_dir.glob("*.md"):
        nombre = md.stem.replace("_", " ")
        nrm_nombre = normalizar(nombre)

        encontrado = False
        for sec in index_data["secciones"]:
            if normalizar(sec["titulo"]) in nrm_nombre:
                nuevo_path = destino_base / f"{sec['id']}_{sec['titulo'].replace(' ', '_')}.md"
                shutil.move(str(md), str(nuevo_path))
                print(f"[→] Movido: {md.name} → {nuevo_path.name}")
                encontrado = True
                break
            if "subtemas" in sec:
                for sub in sec["subtemas"]:
                    if normalizar(sub) in nrm_nombre:
                        folder = "02_Instancias_SQL" if "sql" in normalizar(sub) else sec['slug']
                        nuevo_path = destino_base / folder / f"{sub.replace(' ', '_')}.md"
                        nuevo_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(md), str(nuevo_path))
                        print(f"[→] Movido: {md.name} → {nuevo_path}")
                        encontrado = True
                        break
            if encontrado:
                break
        if not encontrado:
            # calcular sugerencias fuzzy
            candidates = []
            for sec in index_data["secciones"]:
                candidates.append((SequenceMatcher(None, nrm_nombre, normalizar(sec["titulo"])).ratio(), sec["titulo"]))
                for sub in sec.get("subtemas", []):
                    candidates.append((SequenceMatcher(None, nrm_nombre, normalizar(sub)).ratio(), sub))
            candidates.sort(reverse=True)
            sugerencias = [c[1] for c in candidates[:3]]
            print(f"[!] No se pudo clasificar: {md.name}. Sugerencias: {sugerencias}")


if __name__ == "__main__":
    main()
