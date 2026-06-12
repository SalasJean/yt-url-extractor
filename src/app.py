from __future__ import annotations

import logging
import os
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from src.config import (
    DARK_ACCENT,
    DARK_BG,
    DARK_BTN,
    DARK_BTN_HOVER,
    DARK_PANEL,
    DARK_PRIMARY,
    DARK_PRIMARY_HOVER,
    DARK_TEXT,
    FILE_DIALOG_TITLE,
    FILE_DIALOG_TYPES,
    OUTPUT_DEFAULT_NAME,
    OUTPUT_DIALOG_TITLE,
    OUTPUT_DIALOG_TYPES,
)
from src.extractor import batch_search, read_document
from src.models import SearchResult

logger = logging.getLogger(__name__)


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("YouTube URL Extractor Pro")
        self._center_window(650, 550)
        self.root.resizable(False, False)
        self.root.configure(bg=DARK_BG)

        self._ruta_archivo = tk.StringVar()
        self._ejecutando = False

        self._fonts = {
            "title": ("Segoe UI", 12, "bold"),
            "normal": ("Segoe UI", 10),
            "console": ("Consolas", 10),
        }

        self._build_ui()

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------
    def _center_window(self, width: int, height: int) -> None:
        self.root.update_idletasks()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _build_ui(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TProgressbar",
            thickness=8,
            background=DARK_ACCENT,
            troughcolor=DARK_PANEL,
            bordercolor=DARK_BG,
        )

        header = tk.Label(
            self.root,
            text="YouTube URL Extractor",
            bg=DARK_BG,
            fg=DARK_TEXT,
            font=("Segoe UI", 18, "bold"),
        )
        header.pack(pady=(25, 15))

        frame_file = tk.Frame(
            self.root,
            bg=DARK_PANEL,
            padx=20,
            pady=20,
            highlightbackground="#44475a",
            highlightthickness=1,
        )
        frame_file.pack(fill="x", padx=30, pady=10)

        label = tk.Label(
            frame_file,
            text="Carga tu lista de canciones (.txt o .docx):",
            bg=DARK_PANEL,
            fg=DARK_TEXT,
            font=self._fonts["normal"],
        )
        label.pack(anchor="w", pady=(0, 8))

        input_row = tk.Frame(frame_file, bg=DARK_PANEL)
        input_row.pack(fill="x")

        self._entry_ruta = tk.Entry(
            input_row,
            textvariable=self._ruta_archivo,
            font=self._fonts["normal"],
            bg="#44475a",
            fg=DARK_TEXT,
            insertbackground=DARK_TEXT,
            relief="flat",
            state="readonly",
        )
        self._entry_ruta.pack(side="left", padx=(0, 15), expand=True, fill="x", ipady=6)

        btn_buscar = tk.Button(
            input_row,
            text="Examinar",
            command=self._select_file,
            bg=DARK_BTN,
            fg=DARK_TEXT,
            font=self._fonts["title"],
            relief="flat",
            cursor="hand2",
            activebackground=DARK_BTN_HOVER,
            activeforeground="white",
        )
        btn_buscar.pack(side="right", ipadx=15)

        frame_progress = tk.Frame(self.root, bg=DARK_BG)
        frame_progress.pack(fill="both", expand=True, padx=30, pady=10)

        self._console = tk.Text(
            frame_progress,
            height=10,
            state="disabled",
            bg="#000000",
            fg=DARK_ACCENT,
            font=self._fonts["console"],
            relief="flat",
            highlightbackground="#44475a",
            highlightthickness=1,
            padx=10,
            pady=10,
        )
        self._console.pack(fill="both", expand=True, pady=(0, 15))

        self._progress = ttk.Progressbar(
            frame_progress, orient="horizontal", mode="determinate", style="TProgressbar"
        )
        self._progress.pack(fill="x")

        self._btn_iniciar = tk.Button(
            self.root,
            text="EXTRAER URLs A TXT",
            command=self._start_extraction_thread,
            bg=DARK_PRIMARY,
            fg=DARK_PANEL,
            font=("Segoe UI", 13, "bold"),
            relief="flat",
            cursor="hand2",
            activebackground=DARK_PRIMARY_HOVER,
            activeforeground="white",
        )
        self._btn_iniciar.pack(fill="x", padx=30, pady=(10, 30), ipady=12)

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------
    def _log(self, message: str) -> None:
        self._console.config(state="normal")
        self._console.insert(tk.END, message + "\n")
        self._console.see(tk.END)
        self._console.config(state="disabled")

    # ------------------------------------------------------------------
    # File selection
    # ------------------------------------------------------------------
    def _select_file(self) -> None:
        archivo = filedialog.askopenfilename(
            title=FILE_DIALOG_TITLE,
            filetypes=FILE_DIALOG_TYPES,
        )
        if archivo:
            self._ruta_archivo.set(archivo)
            self._log(f"[+] Archivo origen: {os.path.basename(archivo)}")

    # ------------------------------------------------------------------
    # Thread management
    # ------------------------------------------------------------------
    def _start_extraction_thread(self) -> None:
        if not self._ruta_archivo.get():
            messagebox.showwarning(
                "Archivo faltante",
                "Por favor, selecciona primero el archivo (.txt o .docx).",
            )
            return
        if self._ejecutando:
            return

        output_path = filedialog.asksaveasfilename(
            title=OUTPUT_DIALOG_TITLE,
            defaultextension=".txt",
            filetypes=OUTPUT_DIALOG_TYPES,
            initialfile=OUTPUT_DEFAULT_NAME,
        )
        if not output_path:
            return

        self._ejecutando = True
        self._btn_iniciar.config(
            state="disabled",
            bg=DARK_BTN,
            text="PROCESANDO... POR FAVOR ESPERA",
        )
        threading.Thread(
            target=self._run_extraction,
            args=(Path(self._ruta_archivo.get()), Path(output_path)),
            daemon=True,
        ).start()

    # ------------------------------------------------------------------
    # Extraction (runs in background thread)
    # ------------------------------------------------------------------
    def _on_progress(self, current: int, total: int, result: SearchResult) -> None:
        def _update() -> None:
            self._progress.config(value=current)
            if result.found:
                self._log(f"[{current}/{total}] URL extraída: {result.url}")
            elif result.error:
                self._log(f"[{current}/{total}] ERROR: {result.query} — {result.error}")

        self.root.after(0, _update)

    def _run_extraction(self, input_path: Path, output_path: Path) -> None:
        try:
            queries = read_document(input_path)
            if not queries:
                msg = "[-] El documento está vacío o no se pudo leer."
                self.root.after(0, lambda: self._log(msg))
                return

            total = len(queries)
            self.root.after(0, lambda: self._progress.config(maximum=total, value=0))
            self.root.after(0, lambda: self._log(f"[*] Procesando {total} pistas...\n"))

            results = batch_search(queries, progress_callback=self._on_progress)

            with output_path.open("w", encoding="utf-8") as f:
                for r in results:
                    line = (r.url if r.found else f"No encontrado: {r.query}") + "\n"
                    f.write(line)

            msg = f"\n[✓] Listo: {output_path.name}"
            self.root.after(0, lambda: self._log(msg))
            self.root.after(
                0,
                lambda: messagebox.showinfo(
                    "Proceso Exitoso",
                    "Se ha generado el archivo con las URLs correctamente.",
                ),
            )
        except Exception as exc:
            logger.exception("Error crítico en la extracción")
            error_msg = str(exc)
            self.root.after(0, lambda: self._log(f"\n[X] Error crítico: {error_msg}"))
        finally:
            self._ejecutando = False
            self.root.after(
                0,
                lambda: self._btn_iniciar.config(
                    state="normal",
                    bg=DARK_PRIMARY,
                    text="EXTRAER URLs A TXT",
                ),
            )
