#!/usr/bin/env python3
"""Generuje dokumentację HTML pakietu.

Uruchomienie::

    python scripts/generuj_dokumentacje.py

Wynik: ``docs/html/index.html``

:author: Stanisław Kwak
:license: MIT
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _oczekiwane_html(src_pkg: Path, out_pkg: Path) -> set[Path]:
    """Zwraca zbiór plików HTML, które powinny istnieć po generacji pdoc."""

    oczekiwane: set[Path] = set()
    for py in src_pkg.rglob("*.py"):
        rel = py.relative_to(src_pkg)
        if rel.name == "__init__.py":
            if rel.parent == Path("."):
                oczekiwane.add(out_pkg.with_suffix(".html"))
            else:
                oczekiwane.add(out_pkg / rel.parent.with_suffix(".html"))
        else:
            oczekiwane.add(out_pkg / rel.with_suffix(".html"))
    return oczekiwane


def _usun_przestarzale(out: Path, oczekiwane: set[Path]) -> list[Path]:
    """Usuwa pliki HTML nieodpowiadające aktualnym modułom Python."""

    usuniete: list[Path] = []
    rep = out / "repozytorium"
    if not rep.exists():
        return usuniete
    for html in rep.rglob("*.html"):
        if html not in oczekiwane:
            html.unlink()
            usuniete.append(html)
    return usuniete


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    src_pkg = root / "src" / "repozytorium"
    out = root / "docs" / "html"
    out.mkdir(parents=True, exist_ok=True)

    env = {"PYTHONPATH": str(root / "src")}
    cmd = [
        sys.executable,
        "-m",
        "pdoc",
        "repozytorium",
        "-o",
        str(out),
        "--docformat",
        "google",
    ]
    subprocess.run(cmd, cwd=root, env={**dict(__import__("os").environ), **env}, check=True)

    oczekiwane = _oczekiwane_html(src_pkg, out / "repozytorium")
    usuniete = _usun_przestarzale(out, oczekiwane)
    if usuniete:
        print("Usunięto przestarzałe pliki HTML:")
        for path in sorted(usuniete):
            print(f"  - {path.relative_to(root)}")

    print(f"Dokumentacja: {out / 'index.html'}")


if __name__ == "__main__":
    main()
