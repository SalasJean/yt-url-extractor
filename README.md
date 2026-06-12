# YouTube URL Extractor

> Toma una lista de canciones en TXT o DOCX y obtiene automáticamente la URL de YouTube de cada una.

## Stack

- **Python** 3.10+
- **yt-dlp** — búsqueda y extracción de metadatos de YouTube
- **Tkinter** — interfaz gráfica de escritorio
- **python-docx** — lectura de archivos Word (.docx)
- **Ruff** — linter y formateador
- **pytest** — tests unitarios

## Requisitos

- Python 3.10 o superior
- pip (incluido con Python)

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/SalasJean/yt-url-extractor.git
cd yt-url-extractor

# 2. Crear y activar entorno virtual
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
# source .venv/bin/activate

# 3. Instalar el paquete y sus dependencias
pip install -e .
```

Esto instala automáticamente `yt-dlp` y `python-docx` (definidos en `pyproject.toml`).

## Uso

```bash
python main.py
```

1. Seleccioná el archivo con las canciones (`.txt` o `.docx`, una por línea)
2. Elegí dónde guardar el resultado
3. Hacé click en **EXTRAER URLs A TXT**

La aplicación genera un archivo de texto con las URLs encontradas y crea un `app.log` con el registro de la sesión.

## Tests

```bash
# Instalar dependencias de desarrollo (si no lo hiciste antes)
pip install ruff pytest

# Lint
ruff check src tests

# Ejecutar tests
pytest -v
```

## Estructura del proyecto

```
├── src/
│   ├── config.py      # Constantes, opciones de yt-dlp, colores
│   ├── models.py      # SearchResult (dataclass con type hints)
│   ├── extractor.py   # Lógica de búsqueda en YouTube
│   └── app.py         # Interfaz Tkinter
├── tests/
│   ├── fixtures/      # Datos mock para tests
│   └── test_extractor.py
├── main.py            # Entry point de la aplicación
├── pyproject.toml     # Configuración del proyecto, dependencias, ruff y pytest
└── .gitignore
```

## Licencia

MIT
