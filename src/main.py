"""Szacowanie cen nieruchomości z estońskich ogłoszeń

:author: Stanisław Kwak
:license: MIT
"""

from __future__ import annotations

import flet as ft

from repozytorium.ui.aplikacja import uruchom


def main(page: ft.Page) -> None:
    """Włączanie interfejsu użytkownika"""

    uruchom(page)


if __name__ == "__main__":
    ft.run(main)
