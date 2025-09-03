from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("SimpleMCP")


@mcp.tool()
def now_iso() -> str:
    """Devuelve la hora actual en formato ISO 8601 (UTC)."""
    return datetime.now(timezone.utc).isoformat()


@mcp.tool()
def read_text(path: str, max_chars: int = 2000) -> str:
    """Lee un archivo de texto y devuelve hasta max_chars caracteres.
    Rechaza archivos binarios o muy grandes.
    """
    p = Path(path).expanduser().resolve()


    if not p.exists():
        raise FileNotFoundError(f"No existe: {p}")


    if p.stat().st_size > 1_000_000:
        raise ValueError("Archivo demasiado grande (>1 MB)")


    if any(p.suffix.lower() in ext for ext in [".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".exe", ".dll"]):
        raise ValueError("Solo se permiten textos planos")

    text = p.read_text(encoding="utf-8", errors="replace")
    return text[:max_chars]


if __name__ == "__main__":
    mcp.run()