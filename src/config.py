from __future__ import annotations

YDL_OPTS: dict = {
    "format": "best",
    "noplaylist": True,
    "quiet": True,
    "skip_download": True,
}

SUPPORTED_EXTENSIONS: tuple[str, ...] = (".txt", ".docx")

FILE_DIALOG_TITLE = "Selecciona la lista"
FILE_DIALOG_TYPES = [
    ("Documentos soportados", "*.txt *.docx"),
    ("Texto plano", "*.txt"),
    ("Word Document", "*.docx"),
]

OUTPUT_DIALOG_TITLE = "Guardar URLs generadas"
OUTPUT_DIALOG_TYPES = [("Archivo de Texto", "*.txt")]
OUTPUT_DEFAULT_NAME = "solo_urls.txt"

REQUEST_DELAY = 1.0
REQUEST_DELAY_ON_ERROR = 2.0

DARK_BG = "#1e1e2e"
DARK_PANEL = "#282a36"
DARK_TEXT = "#f8f8f2"
DARK_ACCENT = "#50fa7b"
DARK_BTN = "#6272a4"
DARK_BTN_HOVER = "#7aa2f7"
DARK_PRIMARY = "#bd93f9"
DARK_PRIMARY_HOVER = "#ff79c6"
