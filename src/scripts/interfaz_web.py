#!/usr/bin/env python
"""Interfaz web mínima para lanzar tareas de wiki_modular."""
from __future__ import annotations

import subprocess
import sys

import streamlit as st

from utils.entorno import add_src_to_path, script_path

add_src_to_path()

SCRIPTS = {
    "Procesar nuevos": "procesar_nuevos.py",
    "Iniciar entorno": "iniciar_entorno.py",
    "Validar enlaces": "validar_enlaces_wiki.py",
}


def run_script(name: str) -> subprocess.CompletedProcess[str]:
    """Ejecuta ``name`` y captura la salida."""
    path = script_path(name)
    return subprocess.run(
        [sys.executable, str(path)], capture_output=True, text=True
    )


st.set_page_config(page_title="Wiki Modular")
st.title("Herramientas Wiki Modular")

for label, script in SCRIPTS.items():
    if st.button(label, use_container_width=True):
        with st.spinner(f"Ejecutando {label}..."):
            result = run_script(script)
        if result.returncode == 0:
            st.success(f"✅ {label} completado")
        else:
            st.error(f"❌ {label} falló")
        st.code(result.stdout + "\n" + result.stderr)
