# Guía de contribución

Antes de enviar cambios asegúrese de mantener fuera del control de versiones los archivos temporales y el entorno virtual. La carpeta `.venv/` no debe formar parte del repositorio. Si alguna vez se agregó por error, elimínela con:

```bash
git rm -r --cached .venv/
```

Revise también que directorios como `logs/`, así como `mismatch_report.csv` y `_fuentes/_originales/`, estén listados en `.gitignore`.
