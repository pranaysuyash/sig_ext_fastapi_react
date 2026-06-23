"""Optional parser adapter seams for local-first PDF parsing experiments."""

from __future__ import annotations

from dataclasses import dataclass
import importlib.util
from pathlib import Path
from typing import Any, Dict, List


@dataclass(frozen=True)
class ParserAdapterStatus:
    """Availability and policy snapshot for one parser adapter."""

    name: str
    available: bool
    local_first: bool
    notes: str


class LiteParseAdapter:
    """Adapter seam for the optional LiteParse enrichment path."""

    name = "LiteParse"

    def status(self) -> ParserAdapterStatus:
        available = importlib.util.find_spec("liteparse") is not None
        return ParserAdapterStatus(
            name=self.name,
            available=available,
            local_first=True,
            notes="Optional layout-rich parser adapter. Runs locally when installed.",
        )

    def parse(self, pdf_path: str) -> Dict[str, Any]:
        """Parse a PDF through LiteParse if the package is installed.

        The adapter is intentionally conservative. It is a seam for the
        exploration branch, not a new default dependency path.
        """
        if not Path(pdf_path).exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        status = self.status()
        if not status.available:
            raise RuntimeError("LiteParse is not installed in this environment")

        raise NotImplementedError(
            "LiteParse adapter seam is present, but the package-specific binding has not been wired yet."
        )


class ManagedParserAdapter:
    """Placeholder seam for explicit opt-in managed parsers like LlamaParse."""

    name = "ManagedParser"

    def status(self) -> ParserAdapterStatus:
        return ParserAdapterStatus(
            name=self.name,
            available=False,
            local_first=False,
            notes="Explicit opt-in adapter only; keep behind consent and audit logging.",
        )

