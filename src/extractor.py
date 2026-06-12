from __future__ import annotations

import logging
import time
from collections.abc import Callable
from pathlib import Path

import docx
from yt_dlp import YoutubeDL

from src.config import REQUEST_DELAY, REQUEST_DELAY_ON_ERROR, YDL_OPTS
from src.models import SearchResult

logger = logging.getLogger(__name__)

ProgressCallback = Callable[[int, int, SearchResult], None]


def read_document(path: Path) -> list[str]:
    if path.suffix.lower() == ".docx":
        doc = docx.Document(str(path))
        return [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    with path.open("r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def search_youtube(
    query: str,
    ydl_opts: dict | None = None,
) -> SearchResult:
    opts = {**(ydl_opts or YDL_OPTS)}
    try:
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=False)
            entries = info.get("entries")
            if entries:
                url = entries[0].get("webpage_url", "")
                if url:
                    return SearchResult(query=query, url=url)
        return SearchResult(query=query, error="No se encontraron resultados")
    except Exception as exc:
        logger.exception("Error buscando '%s': %s", query, exc)
        return SearchResult(query=query, error=str(exc))


def batch_search(
    queries: list[str],
    ydl_opts: dict | None = None,
    progress_callback: ProgressCallback | None = None,
) -> list[SearchResult]:
    total = len(queries)
    results: list[SearchResult] = []
    opts = {**(ydl_opts or YDL_OPTS)}

    for index, query in enumerate(queries, start=1):
        result = search_youtube(query, ydl_opts=opts)
        results.append(result)

        if progress_callback:
            progress_callback(index, total, result)

        delay = REQUEST_DELAY_ON_ERROR if result.error else REQUEST_DELAY
        time.sleep(delay)

    return results
