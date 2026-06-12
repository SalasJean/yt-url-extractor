from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SearchResult:
    query: str
    url: str | None = None
    error: str | None = None

    @property
    def found(self) -> bool:
        return self.url is not None
